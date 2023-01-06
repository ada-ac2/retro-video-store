from app import db
from flask import Blueprint, jsonify, make_response, abort, request
from ..models.customer import Customer


# ~~~~~~ validation checkers ~~~~~~
def validate_model(cls, model_id):
    """
    Checks if customer id is correct dtype (int) and if exists in db.
    :params:
    - customer_id
    :returns:
    - response_msg (dict), status_code (int)
    """
    # check if customer id is integer dtype
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} should be an integer dtype"}, 400))
    # fetch customer by id
    model = cls.query.get(model_id)
    if not model:
        return abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))
    else:
        return model

def validate_post_request(request, reqs):
    """
    Validates that http requests satisfy all requirements for POST methods
    :params:
    - request (from client)
    :returns:
    - request_body (if requirements met)
    """
    
    # collect request
    request_body = request.get_json()
    # check if all requirements in request
    for req in reqs:
        if req not in request_body:
            response = f"Request body must include {req}."
            abort(make_response({"details" : response}, 400))
    return request_body

def validate_put_request(request, reqs):
    """
    Validates that http requests satisfy all requirements for PUT methods
    :params:
    - request (from client)
    :returns:
    - request_body (if requirements met)
    """
    
    # collect request
    request_body = request.get_json()
    # check if all requirements in request
    set_request_keys = set(request_body.keys())
    if not set_request_keys.issubset(reqs):
        return abort(make_response({
                "message": f"modifiable must include {reqs}"
        }, 400))
    return request_body

def validate_request_attributes(cls,request_body):
     # unpack request body items
    for key, val in request_body.items():
        # update customer data
        result = cls.update_attr(key, val)
        if not result:
            return abort(make_response({"message": f"{val} is invalid"}, 400))
    return result

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
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

@customers_bp.route("", methods=["POST"])
def create_a_customer():
    reqs = ["name", "postal_code", "phone"]
    request_body = validate_post_request(request,reqs)
    # create new customer
    new_customer = Customer.create_from_dict(request_body)
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.id}, 201)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def modify_a_customer(customer_id):
    
    reqs = {"name", "postal_code", "phone"}
    request_body = validate_put_request(request,reqs)
    result = validate_request_attributes(Customer, request_body)
    if result:
        customer = validate_model(Customer, customer_id)
        db.session.commit()
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return make_response(
        {"id" : customer.id,"message": f"Customer #{customer_id} successfully deleted"}, 200)