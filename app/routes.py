from app import db
from flask import Blueprint, jsonify, make_response, abort, request
from .models.customer import Customer

# initialize customers blueprint
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# ~~~~~~ customers endpoints ~~~~~~
@customers_bp.route("", methods=["GET"])
def display_all_customers():
    # query all customers
    customers = Customer.query.all()
    # initialize response list
    response = []
    for customer in customers:
        response.append(customer.to_dict())
    return jsonify(response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def display_one_customer(customer_id):
    try:
        # check if customer id is int
        customer_id = int(customer_id)
    except:
        abort(make_response({
            "message": f"{customer_id} should be an integer dtype"
        }, 400))
    # retrieve customer
    customer = Customer.retrieve_by_id(customer_id)
    # check if customer exists
    if not customer:
        abort(make_response({
            "message": f"{customer_id} not found"
        }, 404))
    return customer

@customers_bp.route("", methods=["POST"])
def create_a_customer():
    # request requirements
    reqs = ["name", "postal_code", "phone"]
    # collect request
    request_body = request.get_json()
    # check if all requirements not in request
    if not all(x in request_body for x in reqs):
        abort(make_response({
            "message": "name, postal_code and phone required"
        }, 400))
    # create new customer
    new_customer = Customer.create_from_dict(request_body)
    # commit to database
    db.session.add(new_customer)
    db.session.commit()
    return make_response({
        "message": "customer has been successfully created"
    }, 201)

@customers_bp.route("/<customer_id>", methods=["POST"])
def modify_a_customer():
    pass

@customers_bp.route("/<customer_id>", methods=["POST"])
def delete_a_customer():
    pass