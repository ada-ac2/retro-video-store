from flask import Blueprint, jsonify, abort, make_response, request 
from app import db 
from app.models.video import Video 
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime, timedelta, date
import sys

customers_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")

#--------------------------Helper Functions----------------------------------------------
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"{cls.__name__} {model_id} is invalid"}, 400)) 

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))    
    return model 

#----------------Sort fuction---------------------------------
def sort_helper(cls, sort_query, atr = None): 

    if atr == "name":
        sort_query = sort_query.order_by(cls.name.asc())
    elif atr == "registered_at":
        sort_query = sort_query.order_by(cls.registered_at.asc())
    elif atr == "postal_code":
        sort_query = sort_query.order_by(cls.postal_code.asc())
    elif atr == "title":
        sort_query = sort_query.order_by(cls.title.asc())
    elif atr == "release_date":
        sort_query = sort_query.order_by(cls.release_date.asc())
    else: # If user don't specify any attribute, we would sort by id 
        sort_query = sort_query.order_by(cls.id.asc())
    
    return sort_query

#----------------Pagination fuction------------------------------
def pageination_helper(cls, query, count, page_num):
    try:
        count = int(count)
        if page_num is None:
            page_num = 1
        else:
            try:
                page_num = int(page_num)
            except (ValueError):
                page_num =1

        query_page = query.paginate(page=page_num, per_page=count)
    except (TypeError,ValueError):
        query_page = query.paginate(page=1, per_page=sys.maxsize)

    return query_page

def validate_request_body(request_body): 
    if "customer_id" not in request_body or "name" not in request_body \
    or "phone" not in request_body or "postal_code" not in request_body \
        or "video_id" not in request_body:
        abort(make_response("Invalid Request", 400))

#validation for Video route
def validate_video_request_body(request_body): 

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" \
        not in request_body:
        abort(make_response("Invalid Request", 400))

def validate_rental_request_body(request_body):
    if "customer_id" not in request_body:
        abort(make_response(f"Invalid, Request body missing 'customer_id'", 400))
    if "video_id" not in request_body:
        abort(make_response(f"Invalid, Request body missing 'video_id'", 400))

def due_date():
    due_date = date.today() + timedelta(days=7)
    return due_date

######################
######################
#--------Customer-----
######################
#--------------------------- Customer Route Functions -----------------------------------------

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    
    try:
        new_customer = Customer.from_dict(request_body)

    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))
    
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.id}, 201)
    

@customers_bp.route("", methods=["GET"])
def read_all_customers():
    #get a query object for later use
    customer_query = Customer.query
    count = request.args.get("count")
    page_num = request.args.get("page_num")
#sorting customers
    is_sort = request.args.get("sort")
    if is_sort:
        attribute = is_sort 
        customer_query = sort_helper(Customer,customer_query,attribute)

    # validating count and page_num
    customers = pageination_helper(Customer,customer_query,count,page_num).items
        
    customers_response = [] 
    
    for customer in customers: 
        customers_response.append(customer.to_dict())    #use to_dict function to make code more readable
    
    
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"])
def read_one_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    return customer.to_dict(), 200

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    new_customer = validate_model(Customer, customer_id)

    request_body = request.get_json()
    try:
        new_customer.name = request_body["name"]
        new_customer.postal_code = request_body["postal_code"]
        new_customer.phone = request_body["phone"]
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))
    
    db.session.commit() 
    return new_customer.to_dict(), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id): 
    customer = validate_model(Customer, customer_id) 

    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.id}, 200

######################
######################
#--------Video--------
######################
#--------------------------- Video Route Functions -----------------------------------------

@videos_bp.route("", methods=["POST"])
def create_one_video():
    request_body = request.get_json()
    try:
        new_video = Video.from_dict(request_body)
        
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))

    db.session.add(new_video)
    db.session.commit()
    
    return new_video.to_dict(), 201

@videos_bp.route("", methods=["GET"])
def read_all_videos():
    #get a query object for later use
    video_query = Video.query

    is_sort = request.args.get("sort")
    if is_sort:
        attribute = is_sort
        video_query = sort_helper(Video,video_query,attribute)

    videos = video_query.all()
        
    video_response = [] 
    for video in videos: 
        video_response.append(video.to_dict())    #use to_dict function to make code more readable

    return jsonify(video_response), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def read_one_video_by_id(video_id):
    video = validate_model(Video, video_id)

    return video.to_dict(), 200

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    new_video = validate_model(Video, video_id)
    request_body = request.get_json() 

    try:
        new_video.title = request_body["title"]
        new_video.release_date = request_body["release_date"]
        new_video.total_inventory = request_body["total_inventory"]
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))
    
    db.session.commit() 
    return (jsonify(new_video.to_dict()),200)       

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video_by_id(video_id): 
    video = validate_model(Video, video_id) 

    db.session.delete(video)
    db.session.commit()

    return {"id": video.id}, 200

#--------------------------- Rentals Route Functions -----------------------------------------
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    rental_query = Rental.query

    request_body = request.get_json()
    validate_rental_request_body(request_body)

    video_id = request_body["video_id"]
    video = validate_model(Video,video_id)

    customer_id = request_body["customer_id"]
    customer = validate_model(Customer,customer_id)

    return_date = due_date()
    if video.total_inventory - Rental.query.filter_by(video_id=video_id).count() <= 0:
        return {"message": "Could not perform checkout"}, 400
    
    rental = Rental(
        customer_id = request_body["customer_id"],
        video_id=request_body["video_id"],
        due_date= return_date
    )
    

    db.session.add(rental)
    db.session.commit()

    rentals = Rental.query.filter_by(video_id=video_id).count()
    customers_rentals = customer.video

    check_out_video = {
        "video_id": rental.video_id,
        "customer_id": rental.customer_id,
        "due_date": return_date,
        "videos_checked_out_count": len(customers_rentals),
        "available_inventory": video.total_inventory - rentals
    }

    return jsonify (check_out_video), 200



@rentals_bp.route("/check-in", methods=["POST"])
def checkin_videos():
    request_body = request.get_json()
    validate_rental_request_body(request_body)

    customer_id = request_body["customer_id"]
    customer = validate_model(Customer,customer_id)

    video_id = request_body["video_id"]
    video = validate_model(Video,video_id)

    return_date = due_date()

    if video == Rental.query.filter_by(video_id=video_id):
        return {"message": "Could not perform checkout"}, 400
        

    rental = Rental (
        customer_id = customer.id,
        video_id=video.id
    )

    #.count() returns number of rows
    rentals = Rental.query.filter_by(video_id=video_id).count()
    customers_rentals = Rental.query.filter_by(id=video_id).count()

    if customers_rentals == 0:
        return{"message": f"No outstanding rentals for customer 1 and video 1"}, 400
    
    check_in_video = {
        "video_id": rental.video_id,
        "customer_id": rental.customer_id,
        #"due_date": return_date,
        "videos_checked_out_count": (customers_rentals - rentals),
        "available_inventory": video.total_inventory
    }
    db.session.delete(Rental.query.filter_by(
            video_id=video.id, customer_id=customer.id).first())
    db.session.commit()
    if video == check_in_video["video_id"]:
        return{"message": f"Cannot perform checkout"}, 400

    return jsonify(check_in_video), 200

@customers_bp.route("<customer_id>/rentals", methods=["GET"])
def read_customer_rentals(customer_id):
    customer = validate_model(Customer,customer_id)

    video_query = Video.query
    is_sort = request.args.get("sort")
    count = request.args.get("count")
    page_num = request.args.get("page_num")

    #join_query = db.session.query(Video).join(Rental).filter(customer_id = customer.id)
    #sorting customers
    if is_sort:
        attribute = is_sort
        video_query = sort_helper(Video,video_query,attribute)

    # validating count and page_num
    #video_rentals = pageination_helper(Video,video_query,count,page_num).items
    
    customer_rentals_response = []

    for video in video_query:

        rental = Rental.query.filter_by(
            video_id=video.id,
            customer_id=customer.id
        ).all()
        
        rental_due_date = rental[0].due_date

        customer_rentals_response.append({
            "release_date": video.release_date,
            "id": video.id,
            "title": video.title,
            "due_date": rental_due_date,
            "total_inventory": video.total_inventory
        })

    if customer_rentals_response is None:
        return jsonify([]), 200
    return jsonify(customer_rentals_response), 200


@videos_bp.route("<video_id>/rentals", methods=["GET"])
def read_video_rentals(video_id):
    video = validate_model(Video,video_id)

    customer_query = Customer.query
    is_sort = request.args.get("sort")
    count = request.args.get("count")
    page_num = request.args.get("page_num")

    #sorting customers
    if is_sort:
        attribute = is_sort
        customer_query = sort_helper(Customer,customer_query,attribute)

    # validating count and page_num
    customer_rentals = pageination_helper(Customer,customer_query,count,page_num).items

    video_rentals_response = []

    for customer in customer_rentals:
        rental = Rental.query.filter_by(
            customer_id=customer.id,
            video_id=video.id
        ).first()

        video_rentals_response.append({
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "due_date": rental.due_date,
            "postal_code": customer.postal_code
        })

    if video_rentals_response is None:
        return jsonify([]), 200
    return jsonify(video_rentals_response), 200
