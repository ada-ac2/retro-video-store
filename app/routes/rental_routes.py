from app import db
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer
from app.routes.video_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"]) 
def video_checkout():
    request_body=request.get_json()
    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])
    #put into rental model as to_dictionary
    new_rental=Rental(
        customer_id = customer.id,
        video_id = video.id
    )
    db.session.add(new_rental)
    db.session.commit()

    return make_response(jsonify(new_rental), 200)