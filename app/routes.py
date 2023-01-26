from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request

# Define Blueprints
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# Validation Helper Fns
def validate_request_data_and_create_obj(cls, request_data):
    try:
        new_obj = cls.from_dict(request_data)
    except KeyError as e:
            key = str(e).strip("\'")
            abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))
    return new_obj

def validate_model(cls, model_id):
    
    try:
        model_id = int(model_id)
    except:
        # handling invalid id type
        abort(make_response({"message":f"{cls.__name__} {model_id} was invalid"}, 400))

    # return obj data if id in db
    model = cls.query.get(model_id)

    # handle nonexistant id
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model

# def sorted_rentals_query(sort_request):
    



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
        customers = Customer.query.all()
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
    rental_query = db.session.query(Rental)
    sort_query = request.args.get("sort")
    if sort_query == "title":
        rental_query = Rental.query.order_by(Video.title)
    elif sort_query == "release_date":
        rental_query = Rental.query.order_by(Video.release_date)

    rentals_response = []
    for rental in (
        rental_query
        .join(Video)
        .filter(Rental.customer_id == customer_id)
        .all()
    ):
        video = Video.get_video_by_id(rental.video_id)
        rentals_response.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date
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


##################
##  VIDEO ROUTES  ##
##################

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    new_video = validate_request_data_and_create_obj(Video, request_body)

    db.session.add(new_video)
    db.session.commit()

    return new_video.to_dict(), 201

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = validate_model(Video, video_id)
    return video.to_dict() 

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_all_rentals_for_one_customer(video_id):
    video = validate_model(Video, video_id)
     
    rentals = db.session.query(Rental).join(Video).filter(Rental.video_id == video_id).all()
    rentals_response = []
    for rental in rentals:
        customer = Customer.get_customer_by_id(rental.customer_id)
        rentals_response.append({
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            "due_date": rental.due_date
        })

    return jsonify(rentals_response)   

@videos_bp.route("/<video_id>", methods=["PUT"]) 
def update_one_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()
    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))

    db.session.commit()
    return video.to_dict(), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = validate_model(Video, video_id)

    db.session.delete(video)
    db.session.commit()

    return video.to_dict(), 200


##################
##  RENTAL ROUTES  ##
##################

@rentals_bp.route("/check-out", methods=["POST"])
def create_one_rental():
    request_body = request.get_json()

    # rental request MUST have customer_id and video_id included
    try:
        video_id = request_body["video_id"]
        customer_id = request_body["customer_id"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))

    rental_customer = validate_model(Customer, customer_id)
    rental_video = validate_model(Video, video_id)
    videos_checked_out_count = rental_customer.rental_count() + 1
    available_inventory = rental_video.available_inventory() - 1

    if available_inventory < 0:
        return make_response({"message": "Could not perform checkout"}), 400

    new_rental = Rental(
        customer_id=customer_id, 
        video_id=video_id,
        )

    db.session.add(new_rental)
    db.session.commit()

    return {
        "video_id": new_rental.video_id,
        "customer_id": new_rental.customer_id,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory,
        "due_date": new_rental.due_date
        }, 200

@rentals_bp.route("/check-in", methods=["POST"])
def delete_one_rental():
    request_body = request.get_json()

    # rental request MUST have customer_id and video_id included
    try:
        video_id = request_body["video_id"]
        customer_id = request_body["customer_id"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))
    
    rental_customer = validate_model(Customer, customer_id)
    rental_video = validate_model(Video, video_id)
    videos_checked_out_count = rental_customer.rental_count() - 1
    available_inventory = rental_video.available_inventory() + 1

    rental = Rental.query.filter_by(video_id = rental_video.id, customer_id = rental_customer.id).first()
    if rental:
        db.session.delete(rental)
        db.session.commit()
    else: 
        abort(make_response({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400))

    return {
        "video_id": rental.video_id,
        "customer_id": rental.customer_id,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory,
        }, 200
