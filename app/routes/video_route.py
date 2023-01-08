from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, abort, make_response, request 
from app.routes.customer_route import validate_model
videos_bp = Blueprint("videos_bp",__name__, url_prefix="/videos")

#============================== videos_bp.route =============================
#============================================================================
#GET /videos
@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    response_body = []

    for video in videos:
        response_body.append(video.to_dict())
    return jsonify(response_body)

# POST /videos
@videos_bp.route("", methods=["POST"])
def create_video():
    try:
        request_body = request.get_json()
        new_video = Video.from_dict(request_body)
    except:
        abort(make_response({"details":"Request body must include title.,Request body must include release_date.,Request body must include total_inventory."}, 400))

    db.session.add(new_video)
    db.session.commit()
    
    response_body = new_video.to_dict()
    return make_response(response_body, 201)
# GET /videos/<id>
@videos_bp.route("/<id>", methods=["GET"])
def get_video_by_id(id):
    video = validate_model(Video, id)
    
    return jsonify(video.to_dict())



# DELETE /customers/<id>
@videos_bp.route("/<id>", methods=["DELETE"])
def put_customers_by_id(id):
    customer = validate_model(Customer, id)

    db.session.delete(customer)
    db.session.commit()
    
    return jsonify(customer.to_dict()),200

# PUT /customers/<id>
@videos_bp.route("/<id>", methods=["PUT"])
def delete_customers_by_id(id):
    customer = validate_model(Customer, id)
    try:
        request_body = request.get_json()
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except:
        abort(make_response(jsonify("Bad Request"), 400))

    db.session.commit()
    
    return jsonify(customer.to_dict()),200