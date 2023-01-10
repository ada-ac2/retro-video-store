from flask import Blueprint, jsonify, abort, make_response, request 
from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app.routes.routes_helper import validate_model

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

## `POST /rentals/check-out`
@rentals_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()

    try:
        customer = validate_model(Customer, request_body["customer_id"])
        video = validate_model(Video, request_body["video_id"])
        
        videos_checked_out = db.session.query(Rental).filter_by(video_id=video.id).all()  # look into count method
        available_inventory = 0

        if not videos_checked_out:
            available_inventory = video.total_inventory
        else:
            available_inventory = video.total_inventory - len(videos_checked_out)
            
        if available_inventory == 0:
            abort(make_response({"message":f"Could not perform checkout"}, 400))
        
        new_rental = Rental(customer_id=request_body["customer_id"],
                video_id=request_body["video_id"]
                )
        
        customer.videos_checked_out_count += 1
    except KeyError as key_error:
        abort(make_response({"message":f"Could not perform checkout bc {key_error.args[0]}"}, 400))

    db.session.add(new_rental)
    db.session.add(customer)
    db.session.commit()

    rental_response = new_rental.to_dict()
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    available_inventory -= 1
    rental_response["available_inventory"] = available_inventory
    
    return jsonify(rental_response), 200


#`POST /rentals/check-in`
@rentals_bp.route("/check-in", methods=["POST"])
def delete_and_update_one_rental():
    request_body = request.get_json()

    try:
        customer = validate_model(Customer, request_body["customer_id"])
        video = validate_model(Video, request_body["video_id"])

        rental = db.session.query(Rental).filter_by(video_id=video.id, customer_id=customer.id).first() # if customer has more than two rentals
        # checked_in_rental = validate_model(Rental, {"id": rental.id, "customer_id": rental.customer_id, "video_id": rental.video_id})

        if not rental:
            abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))

        if rental.check_out_status == False:
            abort(make_response({"message":f"Could not perform checkout bc already checked out"}, 400))
        
        videos_checked_out = db.session.query(Rental).filter_by(video_id=video.id).all()  # look into count method, refactor duplicate code
        available_inventory = video.total_inventory - len(videos_checked_out)

        customer.videos_checked_out_count -= 1
        available_inventory += 1
        rental.check_out_status = False
        
    except KeyError as key_error:
        abort(make_response({"message":f"Could not perform checkout bc {key_error.args[0]}"}, 400))

    db.session.add(rental)
    db.session.commit()

    rental_response = rental.to_dict()
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    rental_response["available_inventory"] = available_inventory
        
    return jsonify(rental_response), 200
