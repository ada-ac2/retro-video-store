from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.customer import Customer

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except :
        abort(make_response({"message": f"{model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if model:
        return model
    abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

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

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    
    customer = validate_model(Customer, customer_id)
    
    return {
        "id" : customer.id,
        "name": customer.name,
        "postal_code": customer.postal_code,
        "phone": customer.phone,
        "register_at": customer.register_at, 
        "videos_checked_out_count":customer.videos_checked_out_count
    }

@customers_bp.route("", methods=["POST"])
def create_one_customer():
    request_body = request.get_json()
    try:
        customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
        )
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))

    db.session.add(customer)
    db.session.commit()
    return make_response({"id": customer.id}, 201)




