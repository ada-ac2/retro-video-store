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
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    new_customer = Customer.from_dict(request_body)

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify(f"New Customer {new_customer.name} successfully created"), 201)