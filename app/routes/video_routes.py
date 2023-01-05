from app import db
from app.models.video import Video
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

videos_bp = Blueprint("video_bp", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = validate_request_body(Video, request.get_json())
    new_video = Video.from_dict(request_body)

    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()), 201)

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_query = Video.query

    videos = video_query.all()
    video_response = []
    for video in videos:
        video_response.append(video.to_dict())
    
    return jsonify(video_response)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = validate_model(Video, video_id)
    return jsonify(video.to_dict())

@videos_bp.route("/<video_id>",methods=["PUT"])
def update_one_video(video_id):
    video_info = validate_model(Video, video_id)
    request_body = validate_request_body(Video, request.get_json())

    video_info.title = request_body["title"]
    video_info.release_date = request_body["release_date"]
    video_info.total_inventory = request_body["total_inventory"]

    db.session.commit()

    return make_response(jsonify(video_info.to_dict()), 200)

@videos_bp.route("/<video_id>",methods=["DELETE"])
def delete_one_video(video_id):
    video_info = validate_model(Video, video_id)
    
    db.session.delete(video_info)
    db.session.commit()
    
    return make_response(jsonify(video_info.to_dict()), 200)