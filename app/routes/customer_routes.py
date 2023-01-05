from app import db
from app.models.customer import Customer
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def create_customer():
    customer_data = request.get_json()

    if "name" not in customer_data:
        abort(make_response({"details": "Request body must include name."}, 400))
    if "postal_code" not in customer_data:
        abort(make_response({"details": "Request body must include postal_code."}, 400))
    if "phone" not in customer_data:
        abort(make_response({"details": "Request body must include phone."}, 400))

    new_customer = Customer(
        name=customer_data["name"],
        postal_code=customer_data["postal_code"],
        phone=customer_data["phone"],
        videos_checked_out_count = 0
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify({
        "id": new_customer.id,
        "name": new_customer.name,
        "postal_code": new_customer.postal_code,
        "phone": new_customer.phone,
        "videos_checked_out_count": new_customer.videos_checked_out_count}), 201)

@customers_bp.route("", methods=["GET"])
def get_customers():
    customer_query = Customer.query

    customers = customer_query.all()
    customer_response = []

    for customer in customers:
        customer_response.append({
            "id": customer.id,
            "name": customer.name,
            "registered_at": customer.registered_at,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
            "videos_checked_out_count": customer.videos_checked_out_count
        })
    
    return jsonify(customer_response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "registered_at": customer.registered_at,
        "postal_code": customer.postal_code,
        "phone": customer.phone,
        "videos_checked_out_count": customer.videos_checked_out_count
    })
