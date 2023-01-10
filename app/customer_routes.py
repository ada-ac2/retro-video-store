from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.validation_fns import validate_model, validate_request_data_and_create_obj
from flask import Blueprint, jsonify, abort, make_response, request


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


##################
# CUSTOMER ROUTES #
##################

# POST
@customers_bp.route("", methods = ["POST"])
def create_one_customer():
    request_body = request.get_json()
    new_customer = validate_request_data_and_create_obj(Customer, request_body)

    db.session.add(new_customer)
    db.session.commit()

    return new_customer.to_dict(), 201

# GET
@customers_bp.route("",methods = ["GET"])
def read_all_customers():
    sort_query = request.args.get("sort")
    if sort_query == "name" or sort_query == "registered_at" or sort_query == "postal_code":
        customers = Customer.query.order_by(sort_query)
    else:
        customers = Customer.query.order_by(Customer.id)
    
    
    page_num = request.args.get("page_num")
    count = request.args.get("count")

    if page_num and page_num.isdigit() and count and count.isdigit():
        page_num = int(page_num)
        count = int(count)
        customers = customers.paginate(page=page_num, per_page=count).items
    elif count and count.isdigit():
        count = int(count)
        customers = customers.paginate(page=1, per_page=count).items

    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_all_rentals_for_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    rental_query = db.session.query(Rental).join(Video).filter(Rental.customer_id == customer_id)
    sort_query = request.args.get("sort")
    if sort_query == "title":
        rental_query = rental_query.order_by(Video.title)
    elif sort_query == "release_date":
        rental_query = rental_query.order_by(Video.release_date)
    
    page_num = request.args.get("page_num")
    count = request.args.get("count")

    if page_num and page_num.isdigit() and count and count.isdigit():
        page_num = int(page_num)
        count = int(count)
        rental_query = rental_query.paginate(page=page_num, per_page=count).items
    elif count and count.isdigit():
        count = int(count)
        rental_query = rental_query.paginate(page=1, per_page=count).items

    rentals_response = []
    for rental in rental_query:
        video = Video.get_video_by_id(rental.video_id)
        rentals_response.append({
            "id": video.id,
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date,
            "total_inventory": video.total_inventory
        }
)

    return jsonify(rentals_response)
    

# PUT
@customers_bp.route("/<customer_id>", methods=["PUT"]) 
def update_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.phone = request_body["phone"]
        customer.postal_code = request_body["postal_code"]

    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))
    
    db.session.commit()
    return customer.to_dict()

# DELETE
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer(customer_id):
    customer = validate_model(Customer,customer_id)
    db.session.delete(customer)
    db.session.commit()
    return customer.to_dict()