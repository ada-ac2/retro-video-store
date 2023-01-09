from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from ..models.customer import Customer
from ..models.video import Video
from ..models.rental import Rental
from app.models.validation import validate_model, validate_request, validate_and_process_query_params, create_model_query

# ~~~~~~ initialize customers blueprint ~~~~~~
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# ~~~~~~ customers endpoints ~~~~~~
@customers_bp.route("", methods=["GET"])
def display_all_customers():    
    request_query = request.args.to_dict()
    # collect & process query params from http request
    sort, count, page_num = validate_and_process_query_params(Customer, request_query)
    # collect customers
    customer_query = Customer.query
    # check for additional query params
    if sort:
        # sort asc by given attribute e.g. sort=name
        clause = getattr(Customer, sort) 
        customers = customer_query.order_by(clause.asc())
    else:
        # default is sorted by ascending customer id
        customers = customer_query.order_by(Customer.id.asc())
    if count and not page_num:
        # limit selection of customers to view
        customers = customer_query.limit(count)
    if page_num:
        customers = customer_query.paginate(page=int(page_num), per_page=int(count)).items
    # fill http response list
    response = []
    for customer in customers:
        response.append(customer.to_dict())
    return jsonify(response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def display_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

@customers_bp.route("", methods=["POST"])
def create_a_customer():
    reqs = {"name", "postal_code", "phone"}
    request_body = validate_request(request,reqs)
    # create new customer
    new_customer = Customer.create_from_dict(request_body)
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.id}, 201)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def modify_a_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    reqs = {"name", "postal_code", "phone"}
    request_body = validate_request(request,reqs)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    
    db.session.commit()
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return make_response(
        {"id" : customer.id,"message": f"Customer #{customer_id} successfully deleted"}, 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def display_customer_rentals(customer_id):
    customer = validate_model(Customer, customer_id)
    request_query = request.args.to_dict()
    sort, count, page_num = validate_and_process_query_params(Video, request_query)

    join_query = (
        db.session.query(Rental, Video)
        .join(Video, Rental.video_id==Video.id)
        .filter(Rental.customer_id == customer_id)
    )
    if sort:
        join_query = join_query.order_by(sort)
    else:
        # default sort is ascending rental id
        join_query = join_query.order_by(Rental.id.asc())
    if count and not page_num:
        join_query = join_query.limit(count)
    if page_num:
        join_query = join_query.paginate(page=int(page_num), per_page=int(count)).items

    response_body = []
    for row in join_query:
        response_body.append({
            "id": row.Video.id,
            "title": row.Video.title,
            "total_inventory": row.Video.total_inventory,
            "release_date": row.Video.release_date
        })

    return make_response(jsonify(response_body),200)