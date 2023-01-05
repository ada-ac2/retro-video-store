from app import db
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer
from app.routes.video_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request


rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

#calculate avail inventory
def availabl_inventory(video):
    vids_out = db.session.query(Rental).filter_by(
        video_id=video.id,
        status=Rental.RentalStatus.CHECKOUT)
    return video.total_inventory-len([1 for vid in vids_out])
#response helper function
def rental_response(rental,customer,video):
    rental_response={}
    rental_response["video_id"]=video.id
    rental_response["customer_id"]=customer.id
    rental_response["videos_checked_out_count"]=customer.videos_checked_out_count
    rental_response["available_inventory"] = availabl_inventory(video) #here we need to subtract all rentals associated with video 
    return rental_response


@rentals_bp.route("/check-out", methods=["POST"]) 
def video_checkout():
    request_body=request.get_json()
    #put into rental model as to_dictionary
    try:
        customer = validate_model(Customer, request_body["customer_id"])
        video = validate_model(Video, request_body["video_id"])
        if video.total_inventory == 0:
            abort(make_response({"message":"Could not perform checkout"}, 400))
        new_rental=Rental.from_dict(request_body)
        customer.videos_checked_out_count +=1

    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))
    db.session.add_all([new_rental, customer, video])
    
    db.session.commit()

    return make_response(rental_response(new_rental,customer,video), 200)

@rentals_bp.route("/check_in", methods=["PUT"])
def checkin_video():
    request_body = request.get_json()
