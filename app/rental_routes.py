from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.validation_fns import validate_model, validate_request_data_and_create_obj
from flask import Blueprint, jsonify, abort, make_response, request

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")



##################
##  RENTAL ROUTES  ##
##################

@rentals_bp.route("/check-out", methods=["POST"])
def create_one_rental():
    request_body = request.get_json()

    # rental request MUST have customer_id and video_id included
    try:
        video_id = request_body["video_id"]
        customer_id = request_body["customer_id"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))

    rental_customer = validate_model(Customer, customer_id)
    rental_video = validate_model(Video, video_id)
    videos_checked_out_count = rental_customer.rental_count() + 1
    available_inventory = rental_video.available_inventory() - 1

    if available_inventory < 0:
        return make_response({"message": "Could not perform checkout"}), 400

    new_rental = Rental(
        customer_id=customer_id, 
        video_id=video_id,
        )

    db.session.add(new_rental)
    db.session.commit()

    return {
        "video_id": new_rental.video_id,
        "customer_id": new_rental.customer_id,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory,
        "due_date": new_rental.due_date
        }, 200

@rentals_bp.route("/check-in", methods=["POST"])
def delete_one_rental():
    request_body = request.get_json()

    # rental request MUST have customer_id and video_id included
    try:
        video_id = request_body["video_id"]
        customer_id = request_body["customer_id"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))
    
    rental_customer = validate_model(Customer, customer_id)
    rental_video = validate_model(Video, video_id)
    videos_checked_out_count = rental_customer.rental_count() - 1
    available_inventory = rental_video.available_inventory() + 1

    rental = Rental.query.filter_by(video_id = rental_video.id, customer_id = rental_customer.id).first()
    if rental:
        db.session.delete(rental)
        db.session.commit()
    else: 
        abort(make_response({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400))

    return {
        "video_id": rental.video_id,
        "customer_id": rental.customer_id,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory,
        }, 200