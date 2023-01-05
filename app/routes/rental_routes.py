from app import db
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer
from app.routes.video_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request


rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

def rental_response(rental,customer,video):
    rental_response={}
    rental_response["video_id"]=video.id
    rental_response["customer_id"]=customer.id
    rental_response["videos_checked_out_count"]=customer.videos_checked_out_count
    rental_response["available_inventory"] = video.total_inventory
    return rental_response


@rentals_bp.route("/check-out", methods=["POST"]) 
def video_checkout():
    request_body=request.get_json()
    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])
    video.total_inventory -=1
    customer.videos_checked_out_count +=1
    #put into rental model as to_dictionary
    try:
        new_rental=Rental.from_dict(request_body)

    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))
    db.session.add_all([new_rental, customer, video])
    
    db.session.commit()

    return make_response(rental_response(new_rental,customer,video), 200)