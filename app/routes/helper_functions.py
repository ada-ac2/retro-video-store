from flask import Blueprint, jsonify, abort, make_response, request
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

    return model

def custom_query(cls, approvedsortinig, filters={}):
    #list of accepted sort paramas
    valid_sort=(approvedsortinig)
    custom_querys=None

    #getting sort and pagnation args, with defults and types
    sort=request.args.get('sort', 'id')
    page = None
    count=None

    if request.args.get('page_num'):
        page=request.args.get('page_num', 1, type=int)
    else: page=1

    if request.args.get("count"):
        count=request.args.get("count", 100, type=int)
    else: count=100

    #making id if not valid.
    if sort not in valid_sort: sort= 'id'
    #checking to see if class is the orderby attricute
    order_cls=cls

    if cls is Rental: 
        join_class=None
        if filters.get("customer_id"):
            join_class=Video
        else:
            join_class=Customer
        
        if not hasattr(cls,sort):
            find_att=[Customer,Video,Rental]
            for object in find_att:
                if hasattr(object,sort):
                    order_cls=object
                    break
    
        custom_querys=cls.query.filter_by(**filters).join(join_class).order_by(
            getattr(order_cls,sort)).paginate(page=page,per_page=count,error_out=False)
    else:
        custom_querys=cls.query.order_by(getattr(
            order_cls,sort)).paginate(page,count,False)
    
    query=custom_querys.items
    return query