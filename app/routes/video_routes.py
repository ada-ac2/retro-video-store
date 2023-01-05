from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, abort, make_response, request

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