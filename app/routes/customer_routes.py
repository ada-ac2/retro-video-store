from app import db
from flask import Blueprint, jsonify, make_response, request
from ..models.customer import Customer
from ..models.video import Video
from ..models.rental import Rental
from app.models.validation import validate_model, validate_request, validate_and_process_query_params, create_model_query

# ~~~~~~ initialize customers blueprint ~~~~~~
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# ~~~~~~ customers endpoints ~~~~~~
@customers_bp.route("", methods=["GET"])
def display_all_customers():    
    request_query = request.args.to_dict()
    # collect & process query params from http request
    sort, count, page_num = validate_and_process_query_params(Customer, request_query)
    # collect customers
    customer_query = Customer.query
    # default is sorted by ascending customer id
    customers = customer_query.order_by(Customer.id.asc())
    # check for additional query params
    if sort:
        # sort asc by given attribute e.g. sort=name
        clause = getattr(Customer, sort["sort"])
        customers = customer_query.order_by(clause.asc())
    if count:
        # limit selection of customers to view
        customers = customer_query.limit(count["count"])
    # fill http response list
    response = []
    for customer in customers:
        response.append(customer.to_dict())
    return jsonify(response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def display_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

@customers_bp.route("", methods=["POST"])
def create_a_customer():
    reqs = {"name", "postal_code", "phone"}
    request_body = validate_request(request,reqs)
    # create new customer
    new_customer = Customer.create_from_dict(request_body)
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.id}, 201)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def modify_a_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    reqs = {"name", "postal_code", "phone"}
    request_body = validate_request(request,reqs)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    
    db.session.commit()
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return make_response(
        {"id" : customer.id,"message": f"Customer #{customer_id} successfully deleted"}, 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def display_customer_rentals(customer_id):
    customer = validate_model(Customer, customer_id)
    # collect & process query params from http request
    request_query = request.args.to_dict()
    sort, count, page_num = validate_and_process_query_params(Rental, request_query)
    # collect rentals by customer id
    rental_query = Rental.query.filter_by(customer_id = customer.id)
    # default is sorted by asc rental id
    rentals = rental_query.order_by(Rental.id.asc())
    if count:
        # limit selection of customers to view
        rentals = rental_query.limit(count["count"])
    # fill http response list
    rentals_response = []
    for rental in rentals:
        if rental.status == "checked_out":
            rentals_response.append(rental.to_dict())
    return make_response(jsonify(rentals_response), 200)