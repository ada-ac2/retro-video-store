from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except :
        abort(make_response({"message": f"{model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if model:
        return model
    abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_response = []
    customers = Customer.query.all()
    for customer in customers:
        customers_response.append(customer.to_dict())

    return make_response(jsonify(customers_response), 200) 

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    
    customer = validate_model(Customer, customer_id)
    
    return make_response(jsonify(customer.to_dict()), 200)

@customers_bp.route("", methods=["POST"])
def create_one_customer():
    request_body = request.get_json()
    try:
        customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
        )
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))

    db.session.add(customer)
    db.session.commit()
    return make_response({"id": customer.id}, 201)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))

    db.session.commit()
    return make_response(jsonify(customer.to_dict()),200) 

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.id}


# --------------------------------
# ----------- VIDEOS -------------
# --------------------------------

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos_response = []
    videos = Video.query.all()

    for video in videos:
        videos_response.append(video.to_dict())
    return make_response(jsonify(videos_response), 200)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = validate_model(Video, video_id)

    return make_response(jsonify(video.to_dict()),200)

@videos_bp.route("", methods=["POST"])
def create_one_video():
    request_body = request.get_json()
    try:
        video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
        )
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))
    
    db.session.add(video)
    db.session.commit()

    return make_response({"id":video.id, "title":video.title, "total_inventory":video.total_inventory}, 201)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_one_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()
    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    except KeyError as keyerror:
        abort(make_response({"details":f"Request body must include {keyerror.args[0]}."}, 400))
    
    db.session.commit()

    return make_response(jsonify(video.to_dict()), 200)

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = validate_model(Video, video_id)

    db.session.delete(video)
    db.session.commit()

    return {"id": video.id}


# --------------------------------
# ----------- Rentals -------------
# --------------------------------

@rental_bp.route("/check-out", methods = ["POST"])
def checkout_one_video():
    request_body = request.get_json()
    
    try:
        customer = validate_model(Customer, request_body["customer_id"])
        video = validate_model(Video, request_body["video_id"])

        #avaliable inventory = total inventory - total checkedout  
        available_to_rent = video.total_inventory - Rental.query.filter_by(video_id=video.id).count()
        if available_to_rent < 1: 
            abort(make_response({"message" : "Could not perform checkout"}, 400))
        
        # update customer database 
        customer.videos_checked_out_count += 1
        
        new_rental = Rental(
            customer_id = customer.id,
            video_id = video.id, 
            videos_checked_out_count = customer.videos_checked_out_count, 
            available_inventory = available_to_rent - 1  # Decrement current available_inventory 
        )
    except KeyError as keyerror:
        abort(make_response({"details" : f"Request body must include {keyerror.args[0]}."}, 400))

    db.session.add(new_rental)
    db.session.commit() 

    return make_response(jsonify(new_rental.to_dict()), 200)


@rental_bp.route("/check-in", methods = ["POST"])
def check_in_one_video(): 
    request_body = request.get_json() 

    try:
        customer = validate_model(Customer, request_body["customer_id"])
        video = validate_model(Video, request_body["video_id"])

        # Decrement customer's videos checked out count when they return the video 
        customer.videos_checked_out_count -= 1 
        # Increment inventory when video is returned 
        available_inventory = video.total_inventory - Rental.query.filter_by(video_id=video.id).count() + 1 
        # find the rental record that needs to be deleted 
        to_delete_rental = Rental.query.filter_by(video_id=video.id, customer_id = customer.id).first() 

        if to_delete_rental:
            db.session.delete(to_delete_rental)
            db.session.commit() 
        else: 
            abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))

    except KeyError as keyerror:
        abort(make_response({"details" : f"Request body must include {keyerror.args[0]}."}, 400))

    return {
                "customer_id": customer.id,
                "video_id": video.id,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": available_inventory 
            }, 200 

@customers_bp.route("<id>/rentals", methods = ["GET"])
# List the videos a customer currently has checked out 
def videos_customer_checked_out(id): 
    customer = validate_model(Customer, id)

    list_videos = [] 
    for video in customer.videos:
        list_videos.append(
            {
            "release_date" : video.release_date,
            "title" : video.title, 
            "due_date" : Rental.query.filter_by(customer_id = customer.id, video_id = video.id).first().due_date
            })    

    return make_response(jsonify(list_videos), 200) 

@videos_bp.route("<id>/rentals", methods = ["GET"])
# List the customers who currently have the video checked out
def customers_have_the_video_checked_out(id): 
    video = validate_model(Video, id)
    
    customer_list = []
    for customer in video.customers: 
        customer_list.append(
        {
            "due_date": Rental.query.filter_by(customer_id = customer.id, video_id = video.id).first().due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
        }
        )

    return make_response(jsonify(customer_list), 200) 

