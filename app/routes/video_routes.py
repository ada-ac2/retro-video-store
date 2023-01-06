from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from app.routes.rental_routes import query_rentals
from flask import Blueprint, jsonify, abort, make_response, request

def custom_query(cls, approvedsortinig, filters=None):
    #list of accepted sort paramas
    valid_sort=set(approvedsortinig)
    custom_querys=None

    #getting sort and pagnation args, with defults and types
    sort=request.args.get('sort', 'id')
    page = request.args.get('page',1,type=int)

    count=request.args.get('per_page',100, type=int)
    if request.args.get('count'):
        count=request.args.get('count',100, type=int)
    
    if request.args.get('page_num'):
        page=request.args.get('page_num',1, type=int)

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
    if filters: 
        join_id=None
        join_class=None
        if filters.get("customer_id"):
            join_class=Video
            join_id=join_class.__name__.lower() + "_id"
        elif filters.get("video_id"):
            join_class=Customer
            join_id=join_class.__name__.lower() + "_id"

        if join_class: 
            custom_querys=db.session.query(cls).filter_by(**filters).join(join_class,join_class.id==getattr(
                    cls,join_id), full=True).order_by(
                getattr(order_cls,sort)).paginate(page=page,per_page=count,error_out=False) 

        else:
            custom_querys=db.session.query(cls).filter_by(**filters).order_by(
                getattr(order_cls,sort)).paginate(page,count,False)
        
    elif order_cls !=cls:
            custom_querys=db.sessoin.query(cls).join(join_class,join_class.id==getattr(
                    cls,join_id), full=True).order_by(
                getattr(order_cls,sort)).paginate(page,count,False)
    else:
        custom_querys=cls.query.order_by(getattr(
            order_cls,sort)).paginate(page,count,False)
    
    query=custom_querys.items
    return query


videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

    return model

@videos_bp.route("", methods=["GET"])
def get_all_video():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video_by_id(video_id):
    video = validate_model(Video, video_id)
    return video.to_dict()

@videos_bp.route("", methods=["POST"])
def create_a_video():
    request_body = request.get_json()
    try:
        new_video = Video.from_dict(request_body)
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))
    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_dict(), 201)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_a_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()
    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))
    
    db.session.add(video)
    db.session.commit()

    return make_response(video.to_dict(), 200)

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_a_video(video_id):
    video = validate_model(Video, video_id)

    db.session.delete(video)
    db.session.commit()

    return make_response(jsonify(video.to_dict()), 200)

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rentals_by_video(video_id):
    video = validate_model(Video, video_id)
    query = custom_query(Rental,['id','name','postal_code', 'registered_at'],{"video_id":video.id, "status": Rental.RentalStatus.CHECKOUT})
    
    response = []
    for rental in query:
        customer = validate_model(Customer, rental.customer_id)
        rental_info =  customer.to_dict()
        rental_info["due_date"] = rental.due_date
        response.append(rental_info)
    return jsonify(response)
