from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime

customer_bp = Blueprint("customer_bp", __name__, url_prefix = "/customers")

## Helper functions ##

# Validating the id of the customer: id needs to be int and exists the planet with the id.
# Returning the valid class instance if valid id
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
        #abort(make_response(jsonify(f"{cls.__name__} {model_id} invalid"), 400))
    class_obj = cls.query.get(model_id)
    if not class_obj:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
        #abort(make_response(jsonify(f"{cls.__name__} {model_id} was not found"), 404))
    return class_obj

# Validating the user input to create or update the customer
# Returning the valid JSON if valid input
def validate_input(customer_value):
    invalid_dict = {}
    if "name" not in customer_value \
        or not isinstance(customer_value["name"], str) \
        or customer_value["name"] == "":
        invalid_dict["details"] = "Request body must include name."
    if "postal_code" not in customer_value \
        or not isinstance(customer_value["postal_code"], str) \
        or customer_value["postal_code"] == "":
        invalid_dict["details"] = "Request body must include postal_code."
    if "phone" not in customer_value \
        or not isinstance(customer_value["phone"], str) \
        or customer_value["phone"] == "":
        invalid_dict["details"] = "Request body must include phone."
#        return abort(make_response(jsonify("Invalid request"), 400))  
    return invalid_dict

## Routes functions ##

# Get all customers info (GET /customers)
# Return JSON list
@customer_bp.route("", methods = ["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_list = []
    for customer in customers:
        customers_list.append(customer.to_dict())

    return jsonify(customers_list), 200

# Get the customer info by id (GET /customers/<id>)
# Return info in JSON format
@customer_bp.route("/<customer_id>",methods=["GET"] )
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

# Register a customer info (POST /customers)
# Return sussess message "Customer {name} successfully registered"
@customer_bp.route("", methods = ["POST"])
def register_customer():
    customer_info = request.get_json()
    check_invalid_dict = validate_input(customer_info)

    if check_invalid_dict:
        abort(make_response(jsonify(check_invalid_dict), 400))
    
    new_customer = Customer.from_dict(customer_info)
    
    if not new_customer.videos_checked_out_count:
        new_customer.videos_checked_out_count = 0

    new_customer.registered_at = datetime.now()

    db.session.add(new_customer)
    db.session.commit()
    db.session.refresh(new_customer)
    
    return new_customer.to_dict(), 201
    # return make_response(f"Customer {new_customer.name} successfully registered", 201)
    #return make_response(jsonify(f"Customer {new_customer.name} successfully registered"), 201)    

# Update the customer info by id (PUT /customer/<id>)
# Return sussess message "Customer {id} info successfully udated"
@customer_bp.route("/<customer_id>",methods=["PUT"] )
def update_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = validate_input(request.get_json())

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    customer.registered_at = request_body["registered_at"]
    customer.videos_checked_out_count = request_body["videos_checked_out_count"]    
    
    db.session.commit()
    return make_response(jsonify(f"Customer {customer_id} successfully updated"), 200)   

# Delete the customer info by id (DELETE /customer/<id>)
# Return sussess message "Customer {id} info successfully udated"
@customer_bp.route("/<customer_id>",methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return customer.to_dict()
    #return make_response(jsonify(f"Customer {customer.id} info successfully deleted"), 200)
