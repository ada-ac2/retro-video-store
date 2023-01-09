from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request 
from datetime import datetime


customers_bp = Blueprint("customers_bp",__name__, url_prefix="/customers")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    
    return model

#============================== customers_bp.route =============================
#============================================================================
#GET /customers
@customers_bp.route("", methods=["GET"])
def get_customers():
    
    customer_query = Customer.query.all()
    response_body = []

    for customer in customer_query:
        response_body.append(customer.to_dict())
    return jsonify(response_body)

# POST /customers
@customers_bp.route("", methods=["POST"])
def create_customer():
    try:
        request_body = request.get_json()
        new_customer = Customer.from_dict(request_body)
    except:
        abort(make_response({"details":"Request body must include name.,Request body must include phone.,Request body must include postal_code."}, 400))

    db.session.add(new_customer)
    db.session.commit()
    
    response_body = new_customer.to_dict()
    return make_response(response_body, 201)
# GET /customers/<id>
@customers_bp.route("/<id>", methods=["GET"])
def get_customers_by_id(id):
    customer = validate_model(Customer, id)
    
    return jsonify(customer.to_dict())



# DELETE /customers/<id>
@customers_bp.route("/<id>", methods=["DELETE"])
def put_customers_by_id(id):
    customer = validate_model(Customer, id)

    db.session.delete(customer)
    db.session.commit()
    
    return jsonify(customer.to_dict()),200

# PUT /customers/<id>
@customers_bp.route("/<id>", methods=["PUT"])
def delete_customers_by_id(id):
    customer = validate_model(Customer, id)
    try:
        request_body = request.get_json()
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except:
        abort(make_response(jsonify("Bad Request"), 400))

    db.session.commit()
    
    return jsonify(customer.to_dict()),200


# `GET /customers/<id>/rentals`
@customers_bp.route("/<id>/rentals", methods=["GET"])
def get_rentals_by_customer_id(id):
    customer = validate_model(Customer, id)
    response_body = []
    for rental in customer.rentals:
        response_body.append({"title":rental.video.title})

    
    return jsonify(response_body)