from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.validation_fns import validate_model, validate_request_data_and_create_obj
from flask import Blueprint, jsonify, abort, make_response, request


videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


##################
##  VIDEO ROUTES  ##
##################

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    new_video = validate_request_data_and_create_obj(Video, request_body)

    db.session.add(new_video)
    db.session.commit()

    return new_video.to_dict(), 201

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = validate_model(Video, video_id)
    return video.to_dict() 

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_all_rentals_for_one_customer(video_id):
    video = validate_model(Video, video_id) 
    rental_query = db.session.query(Rental).join(Customer).filter(Rental.video_id == video_id)
    
    sort_query = request.args.get("sort")
    if sort_query == "name":
        rental_query = rental_query.order_by(Customer.name)
    elif sort_query == "postal_code":
        rental_query = rental_query.order_by(Customer.postal_code)
    
    page_num = request.args.get("page_num")
    count = request.args.get("count")
    if page_num and page_num.isdigit() and count and count.isdigit():
        page_num = int(page_num)
        count = int(count)
        rental_query = rental_query.paginate(page=page_num, per_page=count).items
    elif count and count.isdigit():
        count = int(count)
        rental_query = rental_query.paginate(page=1, per_page=count).items
    
    rentals_response = []
    for rental in rental_query:
        customer = Customer.get_customer_by_id(rental.customer_id)
        rentals_response.append({
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            "due_date": rental.due_date
        })

    return jsonify(rentals_response)   

@videos_bp.route("/<video_id>", methods=["PUT"]) 
def update_one_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()
    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))

    db.session.commit()
    return video.to_dict(), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = validate_model(Video, video_id)

    db.session.delete(video)
    db.session.commit()

    return video.to_dict(), 200