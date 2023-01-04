from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def create_customer():
    customer_data = request.get_json()

    new_customer = Customer(
        postal_code = customer_data["postal_code"],
        phone_number = customer_data["phone_number"],
        register_at = datetime.datetime.utcnow()
    )