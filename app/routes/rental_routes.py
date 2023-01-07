from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
# from app.models.customer_rental import CustomerRental
# from app.models.video_rental import VideoRental
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("", methods=["POST"])
def create_rental():
    request_body = request.get_json()

    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])
    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
    )

    db.session.add(new_rental)
    db.session.commit()

    return make_response(jsonify(f"Rental {new_rental.id} successfully created"), 201)

@rentals_bp.route("", methods=["GET"])
def read_all_rentals():
    
    rentals = Rental.query.all()

    rentals_response = []
    for rental in rentals:
        rentals_response.append(
            {
                "id": rental.id
            }
        )
    return jsonify(rentals_response)

@rentals_bp.route("/check-out", methods=["POST"])
def check_out():

    request_body = validate_request_body(Rental, request.get_json())
    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])

    # Check if rental for customer and video already exists
    rental_query = Rental.query.all()
    if rental_query:
        rental_query = Rental.query.filter_by(customer_id=customer.id).filter_by(video_id=video.id)
        if rental_query:
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


    # # Create entry in CustomerRental table
    # new_customer_rental = CustomerRental(
    #     customer_id=customer.id,
    #     rental_id=new_rental.id
    # )
    # db.session.add(new_customer_rental)

    # # Create entry in VideoRental table
    # new_video_rental = VideoRental(
    #     video_id=video.id,
    #     rental_id=new_rental.id
    # )

    # db.session.add(new_video_rental)
    
    # Update customer information
    videos_checked_out_count = 1
    customer.videos_checked_out_count = videos_checked_out_count
    db.session.commit()
    
    return make_response(jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": available_inventory
        }), 200)

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():

    request_body = validate_request_body(Rental, request.get_json())
    customer = validate_model(Customer, request_body["customer_id"])
    video = validate_model(Video, request_body["video_id"])
    
    rental_query = Rental.query.all()
    if not rental_query:
        abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))

    rental_query = Rental.query.filter_by(customer_id=customer.id).filter_by(video_id=video.id)
    if not rental_query:
        abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))
    
    rental_to_remove = rental_query.all()[0]

    # customer_rental_query = CustomerRental.query.filter_by(rental_id=rental_to_remove.id)
    
    # db.session.delete(customer_rental_query[0])

    # video_rental_query = VideoRental.query.filter_by(rental_id=rental_to_remove.id)
    
    # db.session.delete(video_rental_query[0])
    
    # Update customer information
    
    videos_checked_out_count = customer.videos_checked_out_count - 1
    customer.videos_checked_out_count = videos_checked_out_count
    
    db.session.delete(rental_to_remove)
    db.session.commit()

    # Update available inventory
    available_inventory = video.total_inventory - len(video.rentals)

    return make_response(jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory
        }), 200)