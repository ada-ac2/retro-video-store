from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("", methods=["POST"])
def create_rental():
    request_body = request.get_json()

    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])
    new_rental = Rental.from_dict(request_body)

    db.session.add(new_rental)
    db.session.commit()

    return make_response(jsonify(f"Rental {new_rental.id} successfully created"), 201)

@rentals_bp.route("", methods=["GET"])
def read_all_rentals():
    rental_query = Rental.query
    rentals_response = []
    for rental in rental_query:
        rentals_response.append(rental.to_dict())
    return jsonify(rentals_response)

@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    request_body = validate_request_body(Rental, request.get_json())
    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])

    # Check if rental for customer and video already exists
    rental_query = Rental.query.all()
    existing_rentals = []
    if rental_query:
        rental_query = Rental.query.filter_by(customer_id=customer.id).filter_by(video_id=video.id)
        for rental in rental_query:
            existing_rentals.append(rental)

    if existing_rentals:
        abort(make_response({"message": "Could not perform checkout"}, 400))
    
    # Check video's available inventory
    available_inventory = video.total_inventory - len(video.rentals)
    if available_inventory < 1:
        abort(make_response({"message": "Could not perform checkout"}, 400))

    # Create new rental
    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
        )
    db.session.add(new_rental)
    db.session.commit()
    available_inventory = video.total_inventory - len(video.rentals)

    # Update customer information
    customer.videos_checked_out_count += 1
    db.session.commit()
    
    return make_response(jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": new_rental.due_date.strftime("%m-%d-%Y"),
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": available_inventory
        }), 200)

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():

    request_body = validate_request_body(Rental, request.get_json())
    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])
    
    rental_query = Rental.query.all()
    existing_rentals = []

    if rental_query:
        rental_query = Rental.query.filter_by(customer_id=customer.id).filter_by(video_id=video.id)
        for rental in rental_query:
            existing_rentals.append(rental)

    if not existing_rentals:
        abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))

    rental_to_remove = existing_rentals[0]

    customer.videos_checked_out_count -= 1
    
    db.session.delete(rental_to_remove)
    db.session.commit()

    # Update available inventory
    available_inventory = video.total_inventory - len(video.rentals)

    return make_response(jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": available_inventory
        }), 200)