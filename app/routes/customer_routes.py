from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from app.routes.helpers import validate_model, validate_request_body
from flask import Blueprint, jsonify, request, make_response, abort
import datetime


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customer_query = Customer.query

    sort_param = request.args.get("sort")
    if sort_param:
        if sort_param == "name":
            customer_query = customer_query.order_by(Customer.name)
        elif sort_param == "registered_at":
            customer_query = customer_query.order_by(Customer.registered_at)
        elif sort_param == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code)
        else:
            customer_query = customer_query.order_by(Customer.id)
    else:
        customer_query = customer_query.order_by(Customer.id)   

    count_param = request.args.get("count")
    page_num_param = request.args.get("page_num")

    pagination = False
    count = None
    page_num = None
    if count_param and count_param.isdigit():
        count = int(count_param)
        pagination = True

    if page_num_param and page_num_param.isdigit():
        page_num = int(page_num_param)
        pagination = True

    customers = []
    if pagination:
        if page_num is None:
            page_num = 1

        page = customer_query.paginate(per_page=count,page=page_num)
        customers = page.items
    else:
        customers = customer_query.all()
    
    customers_response = [customer.to_dict() for customer in customers]

    return make_response(jsonify(customers_response), 200)


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    customer_data = customer.to_dict()

    return make_response(jsonify(customer_data), 200)


@customers_bp.route("", methods=["POST"])
def add_one_customer():
    request_body = request.get_json()
    required_attributes = ["name", "postal_code", "phone"]

    validate_request_body(request_body, required_attributes)
    
    new_customer = Customer(name=request_body["name"], 
            postal_code=request_body["postal_code"],
            phone=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()
    db.session.refresh(new_customer, ["id"])

    return make_response(jsonify({"id":new_customer.id}), 201)


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    
    return make_response(jsonify({"id":int(customer_id)}), 200)


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = request.get_json()
    required_attributes = ["name", "phone", "postal_code"]

    validate_request_body(request_body, required_attributes)
    
    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]
    db.session.commit()
    response_body = request_body
    response_body['registered_at'] = customer.registered_at

    return make_response(jsonify(response_body), 200)


@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customer_checked_out_videos(customer_id):
    validate_model(Customer, customer_id)

    possible_query_params = {"sort" : "", 
            "count": 0, 
            "page_num": 0}

    for query_param in possible_query_params:
        if query_param in request.args:
            possible_query_params[query_param] = request.args.get(query_param)

    join_query = db.session.query(Rental, Video)\
            .join(Video, Rental.video_id==Video.id)\
            .filter(Rental.customer_id == customer_id)

    sort_params = ["title", "release_date"]
    for param in sort_params:
        if possible_query_params["sort"] == param:
            join_query = join_query.order_by(param)

    if possible_query_params["count"] and \
            possible_query_params["count"].isdigit():
        possible_query_params["count"] = int(possible_query_params["count"])
        if possible_query_params["page_num"] and \
                possible_query_params["page_num"].isdigit():
            possible_query_params["page_num"] = \
                    int(possible_query_params["page_num"])
        else:
            possible_query_params["page_num"] = 1
        join_query = join_query.paginate(
                page=possible_query_params["page_num"], 
                per_page=possible_query_params["count"]).items
    else:
        join_query = join_query.all()

    response_body = []
    for row in join_query:
        response_body.append({
            "id": row.Video.id,
            "title": row.Video.title,
            "total_inventory": row.Video.total_inventory,
            "release_date": row.Video.release_date
        })

    return make_response(jsonify(response_body),200)
