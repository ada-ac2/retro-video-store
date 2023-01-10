from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model
from flask_sqlalchemy import Pagination


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# POST /customers 
@customers_bp.route("",methods=["POST"])
def create_customer():
    customer_data = request.get_json()
    
    ###### refactor ######
    if "name" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include name."}, 400))
    if "postal_code" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include postal_code."}, 400))
    if  "phone" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include phone."}, 400))
        
    new_customer = Customer(
        name = customer_data["name"],
        postal_code = customer_data["postal_code"],
        phone = customer_data["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify(new_customer.to_dict()), 201)


# GET /customers
@customers_bp.route("", methods=["GET"])
def get_customers_optional_query():
    customer_query = Customer.query
    
    ###### refactor ######
    sort_query = request.args.get("sort")
    # check sort
    if sort_query == "name":
        customer_query = customer_query.order_by(Customer.name.asc())
    elif sort_query == "registered_at":
        customer_query = customer_query.order_by(Customer.register_at.asc())
    elif sort_query == "postal_code":
        customer_query = customer_query.order_by(Customer.postal_code.asc())
    else:
        customer_query = customer_query.order_by(Customer.id.asc())
    
    
    count_query = request.args.get("count", type=int)
    page_num_query = request.args.get("page_num", type=int)

    # check count
    if count_query and not page_num_query:
        page = customer_query.paginate(page=1, per_page=count_query)
        customers = page.items
    elif count_query and page_num_query:
        page = customer_query.paginate(page=page_num_query, per_page=count_query)
        customers = page.items
    else:
        customers = customer_query.all()
    
    
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())

    return jsonify(customer_response)


# GET /customers/<id>
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer_to_return = validate_model(Customer,customer_id)

    return customer_to_return.to_dict()


# PUT /customers/<id>
@customers_bp.route("/<customer_id>", methods=["PUT"])
def replace_customer_with_id(customer_id):
    customer = validate_model(Customer,customer_id)
    customer_data = request.get_json()
    
    ###### refactor ######
    if "name" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include name."}, 400))
    if "postal_code" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include postal_code."}, 400))
    if  "phone" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include phone."}, 400))
    
    customer.name = customer_data["name"]
    customer.postal_code = customer_data["postal_code"]
    customer.phone = customer_data["phone"]

    db.session.commit()

    return make_response(customer_data, 200)


# DELETE /customers/<id>
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    customer_to_delete = validate_model(Customer,customer_id)
    db.session.delete(customer_to_delete)
    db.session.commit()
    msg = f"Customer {customer_to_delete.id} successfully deleted"
    return make_response(jsonify({"id":customer_to_delete.id, "message":msg}), 200)


# GET /<customer_id>/rentals
@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def rentals_by_video(customer_id):
    customer = validate_model(Customer, customer_id)
    rentals = customer.videos
    
    customer_rental_response = []
    for rental in rentals:
        customer_rental_response.append(rental.to_dict())
        
    ######## refactor ######
    sort_query = request.args.get("sort")
    # check sort
    if sort_query == "title":
        customer_rental_response = sorted(customer_rental_response, key=lambda v: v['title'])
    elif sort_query == "release_date":
        customer_rental_response = sorted(customer_rental_response, key=lambda v: v['release_date'])
    else:
        customer_rental_response = sorted(customer_rental_response, key=lambda v: v['id'])
        
    count_query = request.args.get("count", type=int)
    page_num_query = request.args.get("page_num",1,type=int)
    # # check count
    if count_query and not page_num_query:
        # get the start and end index based on page number
        start_index = (page_num_query - 1) * count_query
        end_index = start_index + count_query
        items = customer_rental_response[start_index : end_index] 
        page = Pagination(None, page_num_query, count_query, len(items), items)
        customer_rental_response = page.items
    elif count_query and page_num_query:
        start_index = (page_num_query - 1) * count_query
        end_index = start_index + count_query
        items = customer_rental_response[start_index : end_index]
        page = Pagination(None, page_num_query, count_query, len(items), items)
        customer_rental_response = page.items


    return make_response(jsonify(customer_rental_response), 200)
