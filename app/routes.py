from flask import Blueprint, jsonify
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
        response.append(customer.to_dict)
    return jsonify(response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def display_one_customer():
    pass

@customers_bp.route("", methods=["POST"])
def create_a_customer():
    pass

@customers_bp.route("/<customer_id>", methods=["POST"])
def modify_a_customer():
    pass

@customers_bp.route("/<customer_id>", methods=["POST"])
def delete_a_customer():
    pass