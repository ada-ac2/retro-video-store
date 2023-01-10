from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.routes.rental_routes import query_rentals
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes.helper_functions import validate_model, custom_query

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    try:

        new_customer = Customer.from_dict(request_body)
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(new_customer)
    db.session.commit()
    return make_response(new_customer.to_dict(), 201)

#queries customers appends dictionaries, jysonifys list. 

@customers_bp.route('', methods=["GET"])
def get_all_customer():
    customers=custom_query(Customer,['id','name','registered_at','postal_code'])
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())
    return jsonify(customer_response)

#get customer by id
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

#route to delete
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify(customer.to_dict()), 200)

#update route
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer=validate_model(Customer, customer_id)
    
    request_body = request.get_json()
    try:

        customer.name=request_body["name"]
        customer.phone=request_body["phone"]
        customer.postal_code=request_body["postal_code"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(customer)
    db.session.commit()

    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    query = custom_query(Rental,['id','title','release_date'],{"customer_id":customer.id, "status": Rental.RentalStatus.CHECKOUT})
    
    response=[]
    for rental in query:
        video = validate_model(Video, rental.video_id)
        rental_info = video.to_dict()
        rental_info["due_date"] = rental.due_date
        response.append(rental_info)
    return jsonify(response)

@customers_bp.route("/<customer_id>/history", methods=["GET"])
def get_video_had_been_checked_out(customer_id):
    customer = validate_model(Customer, customer_id)
    videos = custom_query(Rental,['id','title','release_date'],{"customer_id":customer.id, "status": Rental.RentalStatus.CHECKIN})
    response = []
    rental_info = {}
    for rental in videos:
        video = validate_model(Video, rental.video_id)
        rental_info["title"] = video.title
        rental_info["checkout_date"] = rental.checkout_date
        rental_info["due_date"] = rental.due_date
        response.append(rental_info)
    return jsonify(response)

