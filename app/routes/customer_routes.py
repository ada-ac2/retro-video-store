from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from .validate_routes import validate_model, validate_customer_user_input
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date

customer_bp = Blueprint("customer_bp", __name__, url_prefix = "/customers")

# Get all customers info (GET /customers)
# Return JSON list
@customer_bp.route("", methods = ["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_list = []
    for customer in customers:
        customers_list.append(customer.to_dict())

    return jsonify(customers_list), 200

# Get the customer info by id (GET /customers/<id>)
# Return info in JSON format
@customer_bp.route("/<customer_id>",methods=["GET"] )
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

# Register a customer info (POST /customers)
# Return sussess message "Customer {name} successfully registered"
@customer_bp.route("", methods = ["POST"])
def register_customer():
    customer_info = request.get_json()
    check_invalid_dict = validate_customer_user_input(customer_info)

    if check_invalid_dict:
        abort(make_response(jsonify(check_invalid_dict), 400))
    
    new_customer = Customer.from_dict(customer_info)
    
    if not new_customer.videos_checked_out_count:
        new_customer.videos_checked_out_count = 0

    new_customer.registered_at = date.today()

    db.session.add(new_customer)
    db.session.commit()
    db.session.refresh(new_customer)
    
    return new_customer.to_dict(), 201

# Update the customer info by id (PUT /customer/<id>)
# Return sussess message "Customer {id} info successfully udated"
@customer_bp.route("/<customer_id>",methods=["PUT"] )
def update_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = request.get_json()
    check_invalid_dict = validate_customer_user_input(request_body)
    if check_invalid_dict:
        return abort(make_response(jsonify(check_invalid_dict), 400))
    
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()
    db.session.refresh(customer)

    return customer.to_dict()

# Delete the customer info by id (DELETE /customer/<id>)
# Return sussess message "Customer {id} info successfully udated"
@customer_bp.route("/<customer_id>",methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return customer.to_dict()

# Get customer rentals by customer_id (GET /customers/<id>/rentals)
# Return list the videos a customer currently has checked out - successful
# Return 404 if customer_id not exist (validate customer_id)

@customer_bp.route("/<customer_id>/rentals",methods=["GET"])
def get_video_rentals_for_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    
    rental_response = {}
    video_list = []
    for video in customer.videos:
        rental_response["release_date"] = video.release_date
        rental_response["title"] = video.title
        rental_response["due_date"] = rental.due_date
        video_list.append(rental_response)
    return video_list
