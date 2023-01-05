from app import db
from app.models.video import Video
from app.routes.customer_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")

@video_bp.route("", methods=["GET"])
def get_all_videos():
    #The API should return an empty array and a status 200 if there are no videos.
    videos = Video.query.all()

    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
        
    return jsonify(videos_response)

@video_bp.route("<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    # The API should return back detailed errors and a status 404: Not Found 
    # if this video does not exist.
    video = validate_model(Video, video_id)

    return video.to_dict()

@video_bp.route("", methods=["POST"])
def create_a_new_video():
    # The API should return back detailed errors and a status 400: Bad Request 
    # if the video does not have any of the required fields to be valid.
    request_body = request.get_json()
    reqs = ["title", "release_date", "total_inventory"]
    #request_body = validate_post_request(request,reqs)
    new_video = Video.from_dict(request_body)
    
    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_dict(), 201)