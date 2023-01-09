from app import db
from flask import Blueprint, jsonify, make_response, request
from ..models.rental import Rental
from ..models.customer import Customer
from ..models.video import Video
from app.models.validation import validate_model, validate_request

# ~~~~~~ initialize rentals blueprint ~~~~~~
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    reqs = {"customer_id", "video_id"}
    request_body = validate_request(request, reqs)

    video_id = request_body["video_id"]
    video = validate_model(Video, video_id)

    customer_id = request_body["customer_id"]
    customer = validate_model(Customer, customer_id)

    if video and customer:
        if video.available_inventory<=0:
            return make_response(jsonify({"message": f"Could not perform checkout"}), 400)

        new_rental = Rental.from_dict(request_body)
        
        new_rental.customer = customer
        new_rental.customer.videos_checked_out_count += 1
        
        new_rental.video = video
        new_rental.video.available_inventory -= 1

        db.session.add(new_rental)
        db.session.commit()

        return make_response(jsonify(new_rental.to_dict()), 200)
    else:
        return make_response(jsonify({"message": f"Video {video_id} or Customer {customer_id} are invalid"}), 404)

@rentals_bp.route("/check-in", methods=["POST"])
def checkin_video():
    reqs = {"customer_id", "video_id"}
    request_body = validate_request(request, reqs)

    video_id = request_body["video_id"]
    video = validate_model(Video, video_id)

    customer_id = request_body["customer_id"]
    customer = validate_model(Customer, customer_id)

    if video and customer:
        rental = Rental.query.filter_by(video_id=video_id, customer_id=customer_id).first()
        if not rental:
            return make_response(jsonify({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}), 400)
    
        if rental.status == "checked_in":
            return make_response(jsonify({"message": f"Cannot check_in video already checked_in"}), 400)

        rental.status = "checked_in"
        rental.customer.videos_checked_out_count -= 1
        rental.video.available_inventory += 1
        
        db.session.commit()
        return make_response(jsonify(rental.to_dict()), 200)
    else:
        # if not found error out 
        return make_response(jsonify({"message": f"Video {video_id} or Customer {customer_id} are not found"}), 400)