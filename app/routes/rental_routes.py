from flask import Blueprint, request, make_response, jsonify, abort
from app.routes.customer_routes import validate_model, validate_request_body
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import datetime, timedelta

MAX_DAYS_RENTALS = 7

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video_to_customer():
    request_body = request.get_json()
    required_data = ["customer_id", "video_id"]
    
    validate_request_body(request_body, required_data)

    valid_customer = validate_model(Customer, request_body["customer_id"])
    valid_video = validate_model(Video, request_body["video_id"])

    if valid_video.available_inventory < 1:
        abort(make_response(jsonify({"message":"Could not perform checkout"}), 400))

    if valid_video in valid_customer.videos:
        abort(make_response(jsonify({"message":"This customer already has this video checked out"}), 400))

    new_rental = Rental(
            customer_id=valid_customer.id, 
            video_id=valid_video.id,
            due_date=datetime.now() + timedelta(days=MAX_DAYS_RENTALS))
    valid_video.available_inventory -= 1
    valid_customer.videos_checked_out_count += 1
    db.session.add(new_rental)
    db.session.commit()

    response_body = {
        "customer_id" : valid_customer.id,
        "video_id" : valid_video.id,
        "due_date" : new_rental.due_date,
        "videos_checked_out_count" : valid_customer.videos_checked_out_count,
        "available_inventory" : valid_video.available_inventory
    }

    return make_response(jsonify(response_body), 200)

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_body = request.get_json(silent=True)
    required_data = ["customer_id", "video_id"]

    validate_request_body(request_body,required_data)

    customer = validate_model(Customer,request_body["customer_id"])
    video = validate_model(Video,request_body["video_id"])
    rental = Rental.query.filter_by(video_id=video.id, customer_id=customer.id).first()

    if not rental:
        msg = f"No outstanding rentals for customer {customer.id} and video {video.id}"
        abort(make_response(jsonify({"message":msg}),400))

    video.available_inventory += 1
    customer.videos_checked_out_count -= 1
    
    db.session.delete(rental)
    db.session.commit()

    response_data = {}
    response_data["video_id"] = video.id
    response_data["customer_id"] = customer.id
    response_data["videos_checked_out_count"] = customer.videos_checked_out_count
    response_data["available_inventory"] = video.available_inventory

    return make_response(jsonify(response_data),200)