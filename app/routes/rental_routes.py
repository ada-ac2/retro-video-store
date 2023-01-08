from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from .validate_routes import validate_model, validate_rental_out, check_inventory, validate_rental_in, check_outstanding_videos
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime, timedelta


rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


# #POST /rentals/check-out
@rental_bp.route("/check-out", methods = ["POST"])
def create_rental_check_out():
    request_body = request.get_json()
    check_rental_out = validate_rental_out(request_body)
    if check_rental_out:
        abort(make_response(jsonify(check_rental_out), 400))

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = validate_model(Customer, customer_id)
    video = validate_model(Video, video_id)
    verify_inventory = check_inventory(video)
    if verify_inventory:
        abort(make_response(jsonify(verify_inventory), 400))

    new_rental = Rental(
                        customer_id = customer.id,
                        video_id = video.id,
                        due_date = datetime.now() + timedelta(days=7)
                        )
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.add(new_rental)
    db.session.commit()
    db.session.refresh(new_rental)
    db.session.refresh(video)
    db.session.refresh(customer)

    rental_response = new_rental.to_dict()
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    rental_response["available_inventory"] = video.available_inventory

    return rental_response, 200    


# #POST /rentals/check-in
@rental_bp.route("/check-in", methods = ["POST"])
def create_rental_check_in():
    request_body = request.get_json()
    check_rental_in = validate_rental_in(request_body)
    if check_rental_in:
        abort(make_response(jsonify(check_rental_in), 400))
    
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = validate_model(Customer, customer_id)
    video = validate_model(Video, video_id)
    check_outstanding = check_outstanding_videos(video, customer)
    if check_outstanding:
        abort(make_response(jsonify(check_outstanding), 400))

    return_rental = Rental.query.filter_by(customer_id=1, video_id=1).order_by(Rental.due_date.asc()).first()
    return_rental.status = "Checked in"
    
    customer.videos_checked_in_count += 1
    customer.videos_checked_out_count -= 1
    video.available_inventory += 1

    db.session.add(return_rental)
    db.session.commit()
    db.session.refresh(return_rental)
    db.session.refresh(video)
    db.session.refresh(customer)
    
    rental_response = return_rental.to_dict()
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    rental_response["available_inventory"] = video.available_inventory

    return rental_response, 200    
