from app import db
from app.models.video import Video
from app.routes.customer_routes import validate_model
from app.routes.customer_routes import validate_request
from flask import Blueprint, jsonify, abort, make_response, request

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")

@video_bp.route("", methods=["GET"])
def get_all_videos():
    
    videos_response = []
    videos = Video.query.all()
    if not videos:
        make_response(jsonify(videos_response), 200)
    
    for video in videos:
        videos_response.append(video.to_dict())
        
    return jsonify(videos_response)

@video_bp.route("<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    
    video = validate_model(Video, video_id)

    return video.to_dict()

@video_bp.route("", methods=["POST"])
def create_a_new_video():
    
    reqs = ["title", "release_date", "total_inventory"]
    request_body = validate_request(request,reqs)
    new_video = Video.from_dict(request_body)
    
    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_dict(), 201)

@video_bp.route("<video_id>", methods=["PUT"])
def update_a_video(video_id):
   
    video = validate_model(Video, video_id)

    reqs = {"title", "release_date", "total_inventory"}
    request_body = validate_request(request,reqs)

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    
    db.session.commit()

    return make_response(video.to_dict(), 200)
    
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video_by_id(video_id):
   
    video = validate_model(Video,video_id)

    db.session.delete(video)
    db.session.commit()

    return make_response({
        "id" : video.id,
        "message": f"Video #{video_id} successfully deleted"
        }, 200)

@video_bp.route("<video_id>/rentals", methods=["GET"])
def get_rentals_by_video_id(video_id):
    
    video = validate_model(Video, video_id)
    rentals_response = []
    for rental in video.rentals:
        rentals_response.append({
            "due_date": rental.due_date,
            "name": rental.customer.name,
            "phone": rental.customer.phone,
            "postal_code": rental.customer.postal_code
        })

    return jsonify(rentals_response)