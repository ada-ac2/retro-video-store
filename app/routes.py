from flask import Blueprint, jsonify
from app.models.customer import Customer

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_response = []
    customers = Customer.query.all()
    for customer in customers:
        customers_response.append({
            "id" : customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
            "register_at": customer.register_at, 
            "videos_checked_out_count":customer.videos_checked_out_count
        })
    return jsonify(customers_response)