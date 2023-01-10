from flask import Blueprint, jsonify, abort, make_response,request
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from app import db
from app.routes.helpers import validate_model, validate_request_body

videos_bp = Blueprint("videos_bp",__name__, url_prefix="/videos")

required_data = ["title","total_inventory","release_date"]

@videos_bp.route("",methods=["GET"])
def get_all_videos():
    videos_query = Video.query

    sort_param = request.args.get("sort")
    if sort_param:
        if sort_param == "title":
            videos_query = videos_query.order_by(Video.title)
        elif sort_param == "total_inventory":
            videos_query = videos_query.order_by(Video.total_inventory)
        elif sort_param == "release_date":
            videos_query = videos_query.order_by(Video.release_date)
        else:
            videos_query = videos_query.order_by(Video.id)
    else:
        videos_query = videos_query.order_by(Video.id)   

    count_param = request.args.get("count")
    page_num_param = request.args.get("page_num")

    pagination = False
    count = None
    page_num = None
    if count_param and count_param.isdigit():
        count = int(count_param)
        pagination = True

    if page_num_param and page_num_param.isdigit():
        page_num = int(page_num_param)
        pagination = True
    
    videos = []
    if pagination:
        if page_num is None:
            page_num = 1

        page = videos_query.paginate(per_page=count,page=page_num)
        videos = page.items
    else:
        videos = videos_query.all()

    videos_response = [video.to_dict() for video in videos]
    return jsonify(videos_response)

@videos_bp.route("/<video_id>",methods=["GET"])
def get_video(video_id):
    video = validate_model(Video,video_id)
    return jsonify(video.to_dict())  

@videos_bp.route("",methods=["POST"])
def create_video():
    request_body = request.get_json(silent=True)
    validate_request_body(request_body,required_data)

    new_video = Video(
            title = request_body["title"],
            total_inventory = request_body["total_inventory"],
            release_date = request_body["release_date"]
    )

    try:
        db.session.add(new_video)
        db.session.commit()

    except:
        msg = "Error creating video in db"
        abort(make_response(jsonify({"message":msg}),500))

    return make_response(jsonify(new_video.to_dict()),201)

@videos_bp.route("/<video_id>",methods=["PUT"])    
def update_video(video_id):
    video = validate_model(Video,video_id)

    request_body = request.get_json(silent=True)
    validate_request_body(request_body,required_data)

    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    db.session.commit()

    return make_response(jsonify(video.to_dict()),200)

@videos_bp.route("/<video_id>",methods=["DELETE"]) 
def delete_video(video_id):
    video = validate_model(Video,video_id)

    db.session.delete(video)
    db.session.commit()

    return make_response(jsonify({"id":video.id}),200)

@videos_bp.route("<video_id>/rentals", methods=["GET"])
def list_customers_renting_video(video_id):
    validate_model(Video,video_id)

    possible_query_params = {"sort" : "", 
            "count": 0, 
            "page_num": 0}

    for query_param in possible_query_params:
        if query_param in request.args:
            possible_query_params[query_param] = request.args.get(query_param)

    join_query = db.session.query(Rental, Customer)\
            .join(Customer, Rental.customer_id==Customer.id)\
            .filter(Rental.video_id == video_id)

    sort_params = ["name", "registered_at", "postal_code"]
    for param in sort_params:
        if possible_query_params["sort"] == param:
            join_query = join_query.order_by(param)

    if possible_query_params["count"] and \
            possible_query_params["count"].isdigit():
        possible_query_params["count"] = int(possible_query_params["count"])
        if possible_query_params["page_num"] and \
                possible_query_params["page_num"].isdigit():
            possible_query_params["page_num"] = \
                    int(possible_query_params["page_num"])
        else:
            possible_query_params["page_num"] = 1
        join_query = join_query.paginate(
                page=possible_query_params["page_num"], 
                per_page=possible_query_params["count"]).items
    else:
        join_query = join_query.all()

    response = []
    for row in join_query:
        response.append({
            "name": row.Customer.name,
            "id": row.Customer.id,
            "phone": row.Customer.phone,
            "postal_code": row.Customer.postal_code,
        })

    return make_response(jsonify(response), 200)