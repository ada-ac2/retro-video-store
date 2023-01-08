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
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

#============================== planets_bp.route =============================
#============================================================================
#GET /customers
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
# POST /customers


# PUT /customers/<id>
# DELETE /customers/<id>