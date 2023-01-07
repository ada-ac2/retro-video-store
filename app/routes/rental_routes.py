from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from .validate_routes import validate_model, validate_customer_user_input
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

#POST /rentals/check-out
@rental_bp.route("/check-out", methods = ["POST"])
def create_rental_check_out(customer_id, video_id):
    customer = validate_model(Customer, customer_id)
    video = validate_model(Video, video_id)

    new_rental = Rental(
                        customer_id = customer.id,
                        video_id = video.id,
                        due_date = datetime.date.today() + datetime.timedelta(days=7)
                        )
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.add(new_rental)
    db.session.commit()
    db.session.refresh(new_rental)
    db.session.refresh(video)
    db.session.refresh(customer)

    rental_response = new_rental.to_dict
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    rental_response["available_inventory"] = video.available_inventory

    return rental_response, 200    


#POST /rentals/check-in
@rental_bp.route("/check-in", methods = ["POST"])
def create_rental_check_in(customer_id, video_id):
    customer = validate_model(Customer, customer_id)
    video = validate_model(Video, video_id)

    return_rental = Rental(
                        customer_id = customer.id,
                        video_id = video.id
                        )
    
    customer.videos_checked_out_count -= 1
    video.available_inventory += 1

    db.session.add(return_rental)
    db.session.commit()
    db.session.refresh(return_rental)
    db.session.refresh(video)
    db.session.refresh(customer)
    
    rental_response = return_rental.to_dict
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    rental_response["available_inventory"] = video.available_inventory

    return rental_response, 200    
