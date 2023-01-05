from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, abort, make_response, request

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")

@video_bp.route("", methods=["GET"])
def get_all_videos():

    videos = Video.query.all()

    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
        
    return jsonify(videos_response)

@video_bp.route("<video_id>", methods=["GET"])
def get_video_by_id(video_id):

    video = validate_model(Video, video_id)

    return video.to_dict()

@video_bp.route("", methods=["POST"])
def create_a_new_video():
    request_body = request.get_json()
    new_video = Video.from_dict(request_body)
    
    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(f"Video {new_.video} successfully created"), 201)