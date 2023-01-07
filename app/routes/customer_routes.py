from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def create_customer():
    customer_data = request.get_json()

    if "name" not in customer_data:
        abort(make_response({"details": "Request body must include name."}, 400))
    if "postal_code" not in customer_data:
        abort(make_response({"details": "Request body must include postal_code."}, 400))
    if "phone" not in customer_data:
        abort(make_response({"details": "Request body must include phone."}, 400))

    new_customer = Customer(
        name=customer_data["name"],
        postal_code=customer_data["postal_code"],
        phone=customer_data["phone"],
        videos_checked_out_count = 0
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify({
        "id": new_customer.id,
        "name": new_customer.name,
        "postal_code": new_customer.postal_code,
        "phone": new_customer.phone,
        "videos_checked_out_count": new_customer.videos_checked_out_count}), 201)

@customers_bp.route("", methods=["GET"])
def get_customers():
    customer_query = Customer.query

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "name":
            customer_query = customer_query.order_by(Customer.name.asc())
        elif sort_query == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code.asc())
        elif sort_query == "invalid":
            customer_query = customer_query.order_by(Customer.id.asc())
    else:
        customer_query = customer_query.order_by(Customer.id.asc())
    
    count_query = request.args.get("count")
    if count_query:
        if count_query == "invalid":
            customer_query = customer_query
        else:
            customer_query = customer_query.limit(count_query)
    
    page_num_query = request.args.get("page_num")
    if page_num_query:
        if page_num_query == "invalid":
            customer_query = customer_query
        else:
            offset_query = str(int(count_query) * (int(page_num_query) - 1))
            customer_query = customer_query.offset(offset_query)

    customers = customer_query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())

    return jsonify(customer_response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return jsonify({
        "id": customer.id,
        "name": customer.name,
        "registered_at": customer.registered_at,
        "postal_code": customer.postal_code,
        "phone": customer.phone,
        "videos_checked_out_count": customer.videos_checked_out_count
    })

@customers_bp.route("/<customer_id>",methods=["PUT"])
def update_one_customer(customer_id):
    customer_info = validate_model(Customer, customer_id)
    request_body = validate_request_body(Customer, request.get_json())

    customer_info.name = request_body["name"]
    customer_info.postal_code = request_body["postal_code"]
    customer_info.phone = request_body["phone"]

    db.session.commit()

    return make_response(jsonify(customer_info.to_dict()), 200)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer(customer_id):
    customer_info = validate_model(Customer, customer_id)
    
    db.session.delete(customer_info)
    db.session.commit()
    
    return make_response(jsonify(customer_info.to_dict()), 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_current_rentals(customer_id):
    validate_model(Customer, customer_id)
    video_query = Video.query.join(Rental, Rental.video_id==Video.id).filter(Rental.customer_id==customer_id)
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "title":
            video_query = video_query.order_by(Video.title.asc())
        elif sort_query == "invalid":
            video_query = video_query.order_by(Video.id.asc())
    else:
        video_query = video_query.order_by(Video.id.asc())
    
    count_query = request.args.get("count")
    if count_query:
        if count_query == "invalid":
            video_query = video_query
        else:
            video_query = video_query.limit(count_query)
    
    page_num_query = request.args.get("page_num")
    if page_num_query:
        if page_num_query == "invalid":
            video_query = video_query
        else:
            offset_query = str(int(count_query) * (int(page_num_query) - 1))
            video_query = video_query.offset(offset_query)
    videos = video_query.all()

    rentals_response = []
    for video in videos:
        rentals_response.append(video.to_dict())
        
    return jsonify(rentals_response)