from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model
from flask_sqlalchemy import Pagination

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

# GET /videos
@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos_query = Video.query
    
    ###### refactor ######
    sort_query = request.args.get("sort")
    # check sort
    if sort_query == "title":
        videos_query = videos_query.order_by(Video.title.asc())
    elif sort_query == "release_date":
        videos_query = videos_query.order_by(Video.release_date.asc())
    else:
        videos_query = videos_query.order_by(Video.id.asc())
    
    
    count_query = request.args.get("count", type=int)
    page_num_query = request.args.get("page_num", type=int)

    # check count
    if count_query and not page_num_query:
        page = videos_query.paginate(page=1, per_page=count_query)
        videos = page.items
    elif count_query and page_num_query:
        page = videos_query.paginate(page=page_num_query, per_page=count_query)
        videos = page.items
    else:
        videos = videos_query.all()

    
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())

    return jsonify(videos_response)


# GET /videos/<id>
@videos_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    video_data = validate_model(Video,video_id)

    return video_data.to_dict()


# POST /videos
@videos_bp.route("", methods=["POST"])
def create_video():
    video_data = request.get_json()
    
    ###### refactor ######
    if "title" not in video_data.keys():
        abort(make_response({"details": f"Request body must include title."}, 400))
    if "release_date" not in video_data.keys():
        abort(make_response({"details": f"Request body must include release_date."}, 400))
    if  "total_inventory" not in video_data.keys():
        abort(make_response({"details": f"Request body must include total_inventory."}, 400))
        
    new_video = Video(
        title = video_data["title"],
        release_date = video_data["release_date"],
        total_inventory = video_data["total_inventory"]
    )
    

    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()), 201)


# PUT /videos/<id>
@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    video = validate_model(Video,video_id)
    video_data = request.get_json()
    
    ###### refactor ######
    if "title" not in video_data.keys():
        abort(make_response({"details": f"Request body must include title."}, 400))
    if "release_date" not in video_data.keys():
        abort(make_response({"details": f"Request body must include release_date."}, 400))
    if  "total_inventory" not in video_data.keys():
        abort(make_response({"details": f"Request body must include total_inventory."}, 400))
        
    video.title = video_data["title"]
    video.release_date =video_data["release_date"]
    video.total_inventory = video_data["total_inventory"]

    db.session.commit()

    return make_response(video_data, 200)


# DELETE /videos/<id>
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_customer_by_id(video_id):
    video_to_delete = validate_model(Video,video_id)
    db.session.delete(video_to_delete)
    db.session.commit()

    msg = f"Customer {video_to_delete.id} successfully deleted"
    return make_response(jsonify({"id":video_to_delete.id, "message":msg}), 200)


# GET /id/rentals
@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def rentals_by_video(video_id):
    video = validate_model(Video, video_id)
    
    rentals = Rental.query.all()
    
    rental_customers_response = []
    for rental in rentals:
        if rental.video_id == video.id:
            customer = Customer.query.get(rental.customer_id)
            rental_customers_response.append({
                                        "id": rental.customer_id,
                                        "due_date": rental.due_date.strftime("%Y-%m-%d"),
                                        "name": customer.name,
                                        "phone": customer.phone,
                                        "postal_code": customer.postal_code,
                                        "register_at": customer.register_at.strftime("%Y-%m-%d")
                                    })
    ######## refactor ######
    sort_query = request.args.get("sort")
    
    # check sort
    if sort_query == "name":
        rental_customers_response = sorted(rental_customers_response, key=lambda c: c['name'])
    elif sort_query == "registered_at":
        rental_customers_response = sorted(rental_customers_response, key=lambda c: c['register_at'])
    elif sort_query == "postal_code":
        rental_customers_response = sorted(rental_customers_response, key=lambda c: c['postal_code'])
    else:
        rental_customers_response = sorted(rental_customers_response, key=lambda c: c['id'])
    
    count_query = request.args.get("count", type=int)
    page_num_query = request.args.get("page_num",1,type=int)    
    # # check count
    if count_query and not page_num_query:
        # get the start and end index based on page number
        start_index = (page_num_query - 1) * count_query
        end_index = start_index + count_query
        items = rental_customers_response[start_index : end_index] 
        page = Pagination(None, page_num_query, count_query, len(items), items)
        rental_customers_response = page.items
    elif count_query and page_num_query:
        start_index = (page_num_query - 1) * count_query
        end_index = start_index + count_query
        items = rental_customers_response[start_index : end_index]
        page = Pagination(None, page_num_query, count_query, len(items), items)
        rental_customers_response = page.items

    return make_response(jsonify(rental_customers_response), 200)
