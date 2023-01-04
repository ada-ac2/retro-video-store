from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))
    return model

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    try:

        new_customer = Customer.from_dict(request_body)
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(new_customer)
    db.session.commit()
    return make_response(new_customer.to_dict(), 201)

#queries customers appends dictionaries, jysonifys list. 
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())
    return jsonify(customer_response)

#get customer by id
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()
