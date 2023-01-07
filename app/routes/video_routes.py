from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from .validate_routes import validate_model, validate_record
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date

video_bp = Blueprint("video", __name__, url_prefix="/videos")

# GET /videos
# The API should return an empty array and a status 200 if there are no videos.
@video_bp.route("", methods=["GET"])
def get_videos():
    videos_response = []
    video_query = Video.query
    videos = video_query.all()
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

# GET /vidoes/<id>
# The API should return back detailed errors and 
# a status 404: Not Found if this video does not exist.
@video_bp.route("/<id>", methods=["GET"])
def get_video_by_id(id):
    video = validate_model(Video, id)
    return video.to_dict()

# POST /videos
# The API should return back detailed errors and 
# a status 400: Bad Request if the video does not have any of 
# the required fields to be valid.
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    check_invalid_record = validate_record(request_body)
    if check_invalid_record:
        abort(make_response(jsonify(check_invalid_record), 400))

    new_video = Video.from_dict(request_body)
    
    db.session.add(new_video)
    db.session.commit()
    db.session.refresh(new_video)
    return new_video.to_dict(), 201

# PUT /videos/<id>
# The API should return back detailed errors and 
# a status 404: Not Found if this video does not exist.
# The API should return back a 400 Bad Request response for 
# missing or invalid fields in the request body.
# For example, if total_inventory is missing or is not a number
@video_bp.route("/<id>", methods=["PUT"])
def update_video(id):
    video = validate_model(Video, id)
    request_body = request.get_json()
    check_invalid_record = validate_record(request_body)
    if check_invalid_record:
        return abort(make_response(jsonify(check_invalid_record), 400))
    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()
    db.session.refresh(video)

    return video.to_dict()

# DELETE /videos/<id>
# The API should return back detailed errors 
# and a status 404: Not Found if this video does not exist.
@video_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    video = validate_model(Video, id)
    db.session.delete(video)
    db.session.commit()
    return video.to_dict()

# GET /videos/<id>/rentals
# List the customers who currently have the video checked out
# validate video_id
@video_bp.route("/<video_id>/rentals",methods=["GET"])
def get_customers_who_rent_the_video(video_id):
    video = validate_model(Video, video_id)

    rentals_query = Rental.query.all()

    customer_list = []
    rental_list = []
    # find all rentals of this customer
    for rental in rentals_query:
        if rental.video_id == video_id:
            rental_list.append(rental)
    
    for rental in rental_list:
        rental_response = {}
        customer = validate_model(Customer, rental.customer_id).to_dict()
        rental_response["name"] = customer.name
        rental_response["phone"] = customer.phone
        rental_response["postal_code"] = customer.postal_code
        rental_response["due_date"] = rental.due_date

        customer_list.append(rental_response)

    return customer_list