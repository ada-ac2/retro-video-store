from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request 

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

GET /customers/<id>
POST /customers
PUT /customers/<id>
DELETE /customers/<id>