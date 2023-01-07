from flask import Blueprint, jsonify, abort, make_response, request 
from app import db 
from app.models.video import Video 
from app.models.customer import Customer
from app.models.rental import Rental
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

#Sort fuction
# def sort_helper(sort_query, atr = None): 
#     if sort_query == customer_query && atr == "id": 
#         sort_query = sort_query.order_by(Customer.id.asc())
#     elif atr != None:
#         #Sort in ascending order by default 
#         sort_query = sort_query.order_by(sort_query.atr.asc())

#     return sort_query

def validate_request_body(request_body): 
    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
        abort(make_response("Invalid Request", 400))

#validation for Video route
def validate_video_request_body(request_body): 

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" \
        not in request_body:
        abort(make_response("Invalid Request", 400))

#validation for Rental routes
#def validate_rental_request_body(request_body):
    #if "customer_id" not in request_body or "video_id" not in request_body:
        #abort(make_response("Invalid Request", 400)) 

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

        if attribute == "name":
            customer_query = customer_query.order_by(Customer.name.asc())
        elif attribute == "registered_at":
            customer_query = customer_query.order_by(Customer.registered_at.asc())
        elif attribute == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code.asc())
        else: # If user don't specify any attribute, we would sort by id 
            customer_query = customer_query.order_by(Customer.id.asc())

    # validating count and page_num
    try:
        count = int(count)
        if page_num is None:
            page_num = 1
        else:
            try:
                page_num = int(page_num)
            except (ValueError):
                page_num =1

        customer_page = customer_query.paginate(page=page_num, per_page=count)
    except (TypeError,ValueError):
        customer_page = customer_query.paginate(page=1, per_page=sys.maxsize)

    customers = customer_page.items
        
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

        if attribute == "title":
            video_query = video_query.order_by(Video.title.asc())
        elif attribute == "release_date":
            video_query = video_query.order_by(Video.release_date.asc())
        else: # If user don't specify any attribute, we would sort by id 
            video_query = video_query.order_by(Video.id.asc())

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
    request_body = request.get_json()
    
    if "customer_id" not in request_body or "video_id" not in request_body:
        return {"message": "Invalid: customer_id or video_id not found in request body"}, 400
    
    video = Video.get_id(request_body["video_id"])
    customer = Customer.get_id(request_body["customer_id"])
    
    if not video or not customer:
        return {"message": "video_id or customer_id not found"}, 404
    
    if not video.get_available_video_inventory():
        return {"message": "Could not perform checkout"}, 400
    
    res = Rental.check_out(
        video_id = video.id,
        customer_id=customer.id
        )

    return res

@rentals_bp.route("/check-in", methods=["POST"])
def checkin_videos():
    request_body = request.get_json()

    no_id = ""
    if "customer_id" not in request_body:
        no_id = "customer_id"
    elif "video_id" not in request_body:
        no_id = "video_id"
    if no_id:
        return {"message": f"Invalid, missing {no_id}."}, 400

    video = Video.get_id(request_body["video_id"])
    customer = Customer.get_id(request_body["customer_id"]) 

    if not video or not customer:
        return {"message": "video_id or customer_id not found"}, 404

    res = Rental.check_in(
        video_id = video.id,
        customer_id = customer.id
    )

    return res

@customers_bp.route("<customer_id>/rentals", methods=["GET"])
def read_customer_rentals(customer_id):
    customer_rentals_response = []
    #using validate_model function to replace the get id #customer = Customer.get_id(customer_id)
    customer = validate_model(Customer,customer_id)
    
    #customer_rentals = Rental.query.filter(Rental.customer_id == customer_id).all()
    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404
    
    rentals = customer.rentals

    res = [rental.to_json() for rental in rentals]

    return jsonify(res), 200

@videos_bp.route("<video_id>/rentals", methods=["GET"])
def read_video_rentals(video_id):
    video_rentals_response = []
    #using validate_model function to replace the get id
    #video = Video.get_id(video_id)   
    video = validate_model(Video,video_id)
    video_rentals = Rental.query.filter(Rental.video_id == video_id).all()
    
    is_sort = request.args.get("sort")

    if not video:
        return {"message": f"Video {video_id} was not found"}, 404

    for rental in video_rentals:
        id = rental.customer_id
        video_rentals_response.append(rental.get_rental_by_video_id(id))

    return jsonify(video_rentals_response), 200