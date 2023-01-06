from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.routes.rental_routes import query_rentals
from flask import Blueprint, jsonify, abort, make_response, request

def custom_query(cls, approvedsortinig, filters=None):
    #list of accepted sort paramas
    valid_sort=(approvedsortinig)
    custom_querys=None

    #getting sort and pagnation args, with defults and types
    sort=request.args.get('sort', 'id')
    page = request.args.get('page_num', 1, type=int)
    count=None
    if request.args.get("count"):
        count=request.args.get("count", 100, type=int)
    else:
        count=request.args.get('per_page', 100, type=int)

    #making id if not valid.
    if sort not in valid_sort: sort= 'id'
    #checking to see if class is the orderby attricute
    order_cls=cls

    if not hasattr(cls,sort):
        find_att=[Customer,Video,Rental]
        for object in find_att:
            if hasattr(object,sort):
                order_cls=object



    #are there filters?
    if request.args.get('filter'):
        filters=request.args.getlist('filter')
    if cls is Rental: 
        join_id=None
        join_class=None
        if filters.get("customer_id"):
            join_class=Video
            join_id=join_class.__name__.lower() + "_id"
        elif filters.get("video_id"):
            join_class=Customer
            join_id=join_class.__name__.lower() + "_id"

            
        custom=db.session.query(cls).filter_by(**filters).join(join_class,join_class.id==getattr(
                cls,join_id), full=True).order_by(
            getattr(order_cls,sort))
        custom_querys=custom.paginate(page,count,False)
    else:
        custom_querys=cls.query.order_by(getattr(
            order_cls,sort)).paginate(page,count,False)
    
    query=custom_querys.items
    return query


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

    return model

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    try:

        new_customer = Customer.from_dict(request_body)
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(new_customer)
    db.session.commit()
    return make_response(new_customer.to_dict(), 201)

#queries customers appends dictionaries, jysonifys list. 

@customers_bp.route('', methods=["GET"])
def get_all_customer():
    customers=custom_query(Customer,['id','name','registered_at','postal_code'])
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())
    return jsonify(customer_response)

#get customer by id
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

#route to delete
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify(customer.to_dict()), 200)

#update route
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer=validate_model(Customer, customer_id)
    
    request_body = request.get_json()
    try:

        customer.name=request_body["name"]
        customer.phone=request_body["phone"]
        customer.postal_code=request_body["postal_code"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(customer)
    db.session.commit()

    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_video(customer_id):
    customer = validate_model(Customer, customer_id)
    query = custom_query(Rental,['id','title','release_date'],{"customer_id":customer.id, "status": Rental.RentalStatus.CHECKOUT})
    
    response=[]
    for rental in query:
        video = validate_model(Video, rental.video_id)
        rental_info = video.to_dict()
        rental_info["due_date"] = rental.due_date
        response.append(rental_info)
    return jsonify(response)

    #@customers_bp