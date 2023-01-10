from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app.routes_helper import validate_model
from flask import Blueprint, jsonify, abort, make_response, request
import datetime

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

# POST
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    checkout_data = request.get_json()

        # check vlaid customer and video
    try:
        customer = validate_model(Customer, checkout_data["customer_id"])
        video = validate_model(Video, checkout_data["video_id"])
    except KeyError as err:
        abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
        
    
    # check if the customer did rent the video
    rentals = Rental.query.all()
    rental_count = 0
    for rental in rentals:
        if rental.video_id == video.id:
            rental_count += 1
        if rental.video_id == video.id and rental.customer_id == customer.id:
            msg = f"Customer {customer.id} is already renting video {video.id}."
            abort(make_response({"message":msg}, 400))
                
                
    # get rental count and determine if customer has already checked out the video
    # rental_count, rental_found = get_rental_count(customer.id, video.id)

    available_inventory = video.total_inventory - rental_count
    # error handling: if there are no videos left to be rented
    if available_inventory <= 0:
        abort(make_response({"message":"Could not perform checkout"}, 400))
    video.available_inventory = available_inventory - 1


    # -------if checkout is successful------
    # updates the amount of videos the customer has checked out in the customer database
    customer.videos_checked_out_count += 1

    
    new_rental = Rental(video_id = video.id,
                        customer_id = customer.id,
                        due_date = datetime.date.today() + datetime.timedelta(days=7)
                        )

    db.session.add(new_rental)
    db.session.commit()
    
    check_out_response = {"customer_id": new_rental.customer_id,
                            "video_id": new_rental.video_id,
                            "due_date": new_rental.due_date.strftime("%Y-%m-%d"),
                            "videos_checked_out_count": customer.videos_checked_out_count,
                            "available_inventory": video.available_inventory
                            } 


    return make_response(jsonify(check_out_response), 200)


# /POST
@rentals_bp.route("/check-in", methods=["POST"])
def checkin_video():
    check_in_data = request.get_json()

        # check vlaid customer and video
    try:
        customer = validate_model(Customer, check_in_data["customer_id"])
        video = validate_model(Video, check_in_data["video_id"])
    except KeyError as err:
        abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
    
    # check if the customer did rent the video
    rentals = Rental.query.all()
    rental_found = False
    rental_count = 0

    for rental in rentals:
        if rental.video_id == video.id:
            rental_count += 1
        if (rental.customer_id == customer.id 
                and rental.video_id == video.id):
                rental_found = True

    for rental in rentals:
        if rental.video_id == video.id and rental.customer_id == customer.id:
            rental_found = True

    # error handling: if no record of rental exists
    if rental_found == False:
            msg = f"No outstanding rentals for customer {customer.id} and video {video.id}"
            abort(make_response({"message":msg}, 400))

    # calculate available inventory and update status of video
    available_inventory = video.total_inventory - rental_count
    video.available_inventory = available_inventory + 1
    
    # remove video from customer's checked out count
    customer.videos_checked_out_count -= 1

    check_in_response = {
    "customer_id": customer.id,
    "video_id": video.id,
    "videos_checked_out_count": customer.videos_checked_out_count,
    "available_inventory": video.available_inventory
    }

    # delete record of rental from database
    Rental.query.filter_by(customer_id=customer.id, video_id = video.id).delete()
    db.session.commit()

    return make_response(jsonify(check_in_response), 200)

