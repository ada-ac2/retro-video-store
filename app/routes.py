from app import db
from flask import Blueprint, jsonify, make_response, abort, request
from .models.customer import Customer


# ~~~~~~ validation checkers ~~~~~~
def validate_customer_id(customer_id):
    """
    Checks if customer id is correct dtype (int) and if exists in db.
    :params:
    - customer_id
    :returns:
    - response_msg (dict), status_code (int)
    """
    # check if customer id is integer dtype
    try:
        customer_id = int(customer_id)
    except:
        abort(make_response({"message": f"{customer_id} should be an integer dtype"}, 400))
    # fetch customer by id
    customer = Customer.retrieve_by_id(customer_id)
    if not customer:
        return abort(make_response({"message": f"{customer_id} not found"}, 404))
    else:
        return customer

def validate_post_request(request):
    """
    Validates that http requests satisfy all requirements for PUT/POST methods
    :params:
    - request (from client)
    :returns:
    - request_body (if requirements met)
    """
    # request requirements for put/post
    reqs = ["name", "postal_code", "phone"]
    # collect request
    request_body = request.get_json()
    # check if all requirements in request
    if all(x in request_body for x in reqs):
        return request_body
    else:
        abort(make_response({
            "message": "name, postal_code and phone required"
        }, 400))

# ~~~~~~ initialize customers blueprint ~~~~~~
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
    customer = validate_customer_id(customer_id)
    return customer.to_dict()

@customers_bp.route("", methods=["POST"])
def create_a_customer():
    request_body = validate_post_request(request)
    # create new customer
    new_customer = Customer.create_from_dict(request_body)
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.id}, 201)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def modify_a_customer(customer_id):
    customer = validate_customer_id(customer_id)
    request_body = request.get_json()
    # unpack request body items
    for key, val in request_body.items():
        # update customer data
        result = customer.update_attr(key, val)
        # check if attr not valid
        if not result:
            return abort(make_response({
                "message": f"{key} is not a modifiable data type for customers"
            }, 400))
    db.session.commit()
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    customer = validate_customer_id(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return make_response(
        {"message": f"Customer #{customer_id} successfully deleted"}, 200
    )