from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request 
from app.routes.customer_route import validate_model
from app.routes.customer_route import validate_num_queries
videos_bp = Blueprint("videos_bp",__name__, url_prefix="/videos")

#============================== videos_bp.route =============================
#============================================================================
#GET /videos
@videos_bp.route("", methods=["GET"])
def get_videos():
    sort_query = request.args.get("sort")
    if sort_query == "title":
        video_query = Video.query.order_by(Video.name)
    elif sort_query == "release_date":
        video_query = Video.query.order_by(Video.release_date)
    
    else:
        video_query = Video.query.order_by(Video.id)


    response_body = []

    for video in video_query:
        response_body.append(video.to_dict())
    return jsonify(response_body)

# POST /videos
@videos_bp.route("", methods=["POST"])
def create_video():
    try:
        request_body = request.get_json()
        new_video = Video.from_dict(request_body)
    except:
        abort(make_response({"details":"Request body must include title.,Request body must include release_date.,Request body must include total_inventory."}, 400))

    db.session.add(new_video)
    db.session.commit()
    
    response_body = new_video.to_dict()
    return make_response(response_body, 201)
# GET /videos/<id>
@videos_bp.route("/<id>", methods=["GET"])
def get_video_by_id(id):
    video = validate_model(Video, id)
    
    return jsonify(video.to_dict())



# DELETE /videos/<id>
@videos_bp.route("/<id>", methods=["DELETE"])
def delete_customers_by_id(id):
    video = validate_model(Video, id)

    db.session.delete(video)
    db.session.commit()
    
    return jsonify(video.to_dict()),200

# PUT /videos/<id>
@videos_bp.route("/<id>", methods=["PUT"])
def put_videos_by_id(id):
    video = validate_model(Video, id)
    try:
        request_body = request.get_json()
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    except:
        abort(make_response(jsonify("Bad Request"), 400))

    db.session.commit()
    
    return jsonify(video.to_dict()),200

## `GET /videos/<id>/rentals`
@videos_bp.route("/<id>/rentals", methods=["GET"])
def get_rentals_by_video_id(id):
    video = validate_model(Video, id)
    customer_query = Rental.query.filter_by(video_id=video.id).join(Customer)
    sort_query = request.args.get("sort")
    if sort_query == "name":
        customer_query = customer_query.order_by(Customer.name)
    elif sort_query == "postal_code":
        customer_query = customer_query.order_by(Customer.postal_code)
    elif sort_query == "registered_at":
        customer_query = customer_query.order_by(Customer.registered_at)
    else:
        customer_query = customer_query.order_by(Customer.id)

    count_query = request.args.get("count")  
    page_num_query = request.args.get("page_num")
    if validate_num_queries(count_query) and validate_num_queries(page_num_query):
        page = customer_query.paginate(page=int(page_num_query), per_page=int(count_query), error_out=False)
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