from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from .validate_routes import validate_model, validate_customer_user_input
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date, timedelta


customer_bp = Blueprint("customer_bp", __name__, url_prefix = "/customers")

# Get all customers info (GET /customers)
# Return JSON list
@customer_bp.route("", methods = ["GET"])
def get_all_customers_with_query():

    customer_query = Customer.query
    number_of_customers = Customer.query.count()

    page_query = request.args.get("page_num")
    count_query = request.args.get("count")
    
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "name":
            customer_query = customer_query.order_by(Customer.name)
        elif sort_query == "registered_at":
            customer_query = customer_query.order_by(Customer.registered_at)
        elif sort_query == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code)

    if count_query and count_query.isdigit():
        if int(count_query) > 0:
            if page_query and page_query.isdigit():
                if int(page_query)>0:
                    if number_of_customers - (int(page_query)-1)*int(count_query) >= 0:
                        customer_query = customer_query.paginate(page=int(page_query), per_page=int(count_query)).items   
                    else: 
                        customer_query = customer_query.limit(int(count_query))
            else:
                customer_query = customer_query.limit(int(count_query))
    
    if not page_query:
        customers = customer_query.all()
    else:
        customers = customer_query

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
    check_invalid_dict = validate_customer_user_input(customer_info)

    if check_invalid_dict:
        abort(make_response(jsonify(check_invalid_dict), 400))

    customer_info["videos_checked_out_count"] = 0
    new_customer = Customer.from_dict(customer_info)
    
    new_customer.registered_at = date.today()

    db.session.add(new_customer)
    db.session.commit()
    db.session.refresh(new_customer)
    
    return new_customer.to_dict(), 201

# Update the customer info by id (PUT /customer/<id>)
# Return sussess message "Customer {id} info successfully udated"
@customer_bp.route("/<customer_id>",methods=["PUT"] )
def update_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = request.get_json()
    
    check_invalid_dict = validate_customer_user_input(request_body)
    if check_invalid_dict:
        abort(make_response(jsonify(check_invalid_dict), 400))
    
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()
    db.session.refresh(customer)

    return customer.to_dict()

# Delete the customer info by id (DELETE /customer/<id>)
# Return sussess message "Customer {id} info successfully udated"
@customer_bp.route("/<customer_id>",methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return customer.to_dict()

# Get customer rentals by customer_id (GET /customers/<id>/rentals)
# Return list the videos a customer currently has checked out - successful
# Return 404 if customer_id not exist (validate customer_id)

@customer_bp.route("/<customer_id>/rentals",methods=["GET"])
def get_video_rentals_for_customer_with_query(customer_id):
    customer = validate_model(Customer, customer_id)
    
    rentals_query = Rental.query.all()
    video_query = Video.query

    number_of_videos = Video.query.count()

    page_query = request.args.get("page_num")
    count_query = request.args.get("count")
    
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "title":
            video_query = video_query.order_by(Video.title)
        elif sort_query == "release_date":
            video_query = video_query.order_by(Video.release_date)
    else:
        video_query = video_query.order_by(Video.id)

    if count_query and count_query.isdigit():
        if int(count_query) > 0:
            if page_query and page_query.isdigit():
                if int(page_query)>0:
                    if number_of_videos - (int(page_query)-1)*int(count_query) >= 0:
                        video_query = video_query.paginate(page=int(page_query), per_page=int(count_query)).items   
                    else: 
                        video_query = video_query.limit(int(count_query))
            else:
                video_query = video_query.limit(int(count_query))
    
    video_list = []
    rental_list = []
    
    if not page_query:
        videos = video_query.all()
    else:
        videos = video_query

# find all rentals of this customer
    for rental in rentals_query:
        if rental.customer_id == customer.id:
            rental_list.append(rental)
    
    for video in videos:
        for rental in rental_list:
            if rental.video_id == video.id:
                temp_dict = dict()
                temp_dict["due_date"] = rental.due_date
                temp_dict["title"] = video.title
                temp_dict["release_date"] = video.release_date
                temp_dict["id"] = video.id
                temp_dict["total_inventory"] = video.total_inventory
                video_list.append(temp_dict)

    return jsonify(video_list), 200


@customer_bp.route("/<customer_id>/history", methods=["GET"])
def get_customers_rental_history(customer_id):
    customer = validate_model(Customer, customer_id)
    rentals_query = Rental.query.all()
    history = list()
    
    for rental in rentals_query:
        if rental.customer_id == customer.id and rental.status == "Checked out" and customer.videos_checked_in_count > 0:
            temp_dict = dict()
            video = validate_model(Video, rental.video_id)
            temp_dict["title"] = video.title
            temp_dict["due_date"] = rental.due_date
            temp_dict["checkout_date"] = rental.due_date - timedelta(days=7)
            history.append(temp_dict)
    
    return jsonify(history)
