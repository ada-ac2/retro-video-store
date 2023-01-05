from flask import Blueprint, jsonify, abort, make_response, request 
from app import db 
from app.models.video import Video 
from app.models.customer import Customer

customer_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
video_bp = Blueprint("video_bp", __name__, url_prefix="/video")
rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rental")

#--------------------------Helper Functions----------------------------------------------
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"{cls.__name__} {model_id} is invalid"}, 400)) 

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))    
    return model 

def validate_request_body(request_body): 

    if "name" not in request_body or "phone" not in request_body or "registered_at" \
        not in request_body or "postal_code" not in request_body:
        abort(make_response("Invalid Request", 400))

#--------------------------- Route Functions -----------------------------------------

@customer_bp.route("", method = ["POST"])
def create_customer():
    request_body = request.get_json()
    validate_request_body(request_body)

    new_customer = Customer.from_dict(request_body)

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify(f"Customer: {new_customer.name} created successfully.", 201))

@customer_bp.route("", method = ["GET"])
def read_all_customers():
    #get a query object for later use
    customer_query = Customer.query

    customers = customer_query.all()
        
    customer_response = [] 
    for customer in customers: 
        customer_response.append(customer.to_dict())    #use to_dict function to make code more readable

    return make_response(jsonify(customer_response), 200)

@customer_bp.route("/<customer_id>", method = {"GET"})
def read_one_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    return (customer.to_dict(),200)

@customer_bp.route("/<customer_id>", method = {"PUT"})
def update_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    request_body = request.get_json() 
    validate_request_body(request_body)

    customer.name = request_body["name"]
    customer.registered_at = request_body["registered_at"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit() 

    return make_response(jsonify(f"Customer: {customer_id} has been updated successfully."), 200) 

@customer_bp.route("/<customer_id>", methods = ["DELETE"])
def delete_customer_by_id(customer_id): 
    customer = validate_model(Customer, customer_id)  

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify(f"Customer: {customer_id} has been deleted successfully."), 200) 
