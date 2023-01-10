from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request

# Validation Helper Fns
def validate_request_data_and_create_obj(cls, request_data):
    try:
        new_obj = cls.from_dict(request_data)
    except KeyError as e:
            key = str(e).strip("\'")
            abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))
    return new_obj

def validate_model(cls, model_id):
    
    try:
        model_id = int(model_id)
    except:
        # handling invalid id type
        abort(make_response({"message":f"{cls.__name__} {model_id} was invalid"}, 400))

    # return obj data if id in db
    model = cls.query.get(model_id)

    # handle nonexistant id
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model
