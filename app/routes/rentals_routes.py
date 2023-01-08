from app import db
from flask import Blueprint, jsonify, make_response, abort, request
from ..models.rental import Rental
from ..models.customer import Customer
from ..models.video import Video
from ..routes.customer_routes import validate_model
from ..routes.customer_routes import validate_request

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
        # update customer.videos_checked_out_count
        new_rental.customer = customer
        new_rental.customer.videos_checked_out_count += 1
        # update video.available_inventory 
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
        # QUERY for rental by video_id and customer _id
        rental = Rental.query.filter(video_id=video_id, customer_id=customer_id)
        # if found check it in ->
        # change status to checked_in
        rental.status = "checked_in"
        # update customer.videos_checked_out_count
        rental.customer.videos_checked_out_count -= 1
        # update video.available_inventory 
        rental.video.available_inventory += 1
        rental.video.update
        return make_response(jsonify(rental.to_dict()), 200)
    else:
        # if not found error out 
        return make_response(jsonify({"message": f"Video {video_id} or Customer {customer_id} are not found"}), 400)