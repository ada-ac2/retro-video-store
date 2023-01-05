from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.routes.rental_routes import query_rentals
from flask import Blueprint, jsonify, abort, make_response, request

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

    return model

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

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

#route to delete
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify(customer.to_dict()), 200)

#update route
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer=validate_model(Customer, customer_id)
    
    request_body = request.get_json()
    try:

        customer.name=request_body["name"]
        customer.phone=request_body["phone"]
        customer.postal_code=request_body["postal_code"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(customer)
    db.session.commit()

    return make_response(customer.to_dict(), 200)