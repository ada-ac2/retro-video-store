from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app import db
from app.routes.routes_helper import validate_model, validate_num_queries

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

# CREATE New Video -- POST
@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    
    try:
        new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"]                    
                    )
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))
    
    db.session.add(new_video)
    db.session.commit()
    
    video_response = new_video.to_dict()
    return jsonify(video_response),201

@videos_bp.route("", methods=["GET"])
def read_all_videos():
    video_query = Video.query
    videos = video_query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response),200

@videos_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = validate_model(Video, video_id)
    return video.to_dict()

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()

    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.commit()
    video_response = video.to_dict()

    return jsonify(video_response),200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = validate_model(Video, video_id)

    video_rentals = db.session.query(Rental).filter_by(video_id=video.id).all()
    

    if video_rentals:
        for rental in video_rentals:
            db.session.delete(rental)
        db.session.commit()

    db.session.delete(video)
    db.session.commit()

    video_response = video.to_dict()
    return jsonify(video_response),200

# `GET /videos/<id>/rentals`
#List the customers who currently have the video checked out
@videos_bp.route("/<id>/rentals", methods=["GET"])
def read_all_customers_for_video_id_rental(id):
    video = validate_model(Video, id)
    customer_query = Rental.query.filter_by(video_id=video.id).join(Customer)

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "name":
            customer_query = customer_query.order_by(Customer.name.asc())
        elif sort_query == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code.asc())
        elif sort_query == "registered_at":
            customer_query = customer_query.order_by(Customer.registered_at.asc())
        else:
            customer_query = customer_query.order_by(Customer.id.asc())

    count_query = request.args.get("count")  # check if count and page/ if only count, display all pages
    page_num_query = request.args.get("page_num")

    if validate_num_queries(count_query) and validate_num_queries(page_num_query):
        # need to check if count_query and page_num query are valid nums

        page = customer_query.paginate(page=int(page_num_query), per_page=int(count_query), error_out=False)
        customer_query = customer_query.all()

        customer_result = []

        for items in page.items:
            customer_result.append(items.customer.to_dict())
        return jsonify(customer_result), 200
    
    if validate_num_queries(count_query) and not validate_num_queries(page_num_query):
        page = customer_query.paginate(per_page=int(count_query), error_out=False)
        customer_query = customer_query.all()
        customer_result = []

        for items in page.items:
            customer_result.append(items.customer.to_dict())
        return jsonify(customer_result), 200

    customer_result = []
    customer_query = customer_query.all()
    for customer in customer_query:
        customer_result.append(customer.customer.to_dict())
    return jsonify(customer_result), 200
