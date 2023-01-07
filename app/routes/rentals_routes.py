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
        new_rental = Rental(video_id=request_body["video_id"],customer_id=request_body["customer_id"])
    
        db.session.add(new_rental)
        db.session.commit()

        return make_response(jsonify(new_rental.to_dict()), 200)
    else:
        return make_response(jsonify({"message": f"Video {video_id} or Customer {customer_id} are invalid"}), 404)