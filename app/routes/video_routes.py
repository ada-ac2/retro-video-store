from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, make_response, request, abort


video_bp = Blueprint("videos", __name__, url_prefix="/videos")


def validate_video(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    return model

# GET /videos
# The API should return an empty array and a status 200 if there are no videos.
@video_bp.route("", methods=["GET"])
def get_videos():
    videos_response = []
    video_query = Video.query
    videos = video_query.all()
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)


# GET /vidoes/<id>
# The API should return back detailed errors and 
# a status 404: Not Found if this video does not exist.
@video_bp.route("/<id>", methods=["GET"])
def get_video_by_id(id):
    video = validate_video(id)
    return video.to_dict()


# POST /videos
# The API should return back detailed errors and 
# a status 400: Bad Request if the video does not have any of 
# the required fields to be valid.
@video_bp.route("", method=["POST"])
def create_video():
    request_body = request.get_json()
    new_video = Video.from_dict(request_body)
    db.session.add(new_video)
    db.session.commit()
    return make_response(jsonify(f"Video {new_video.title} successfully created"), 201)


# PUT /videos/<id>
# The API should return back detailed errors and 
# a status 404: Not Found if this video does not exist.
# The API should return back a 400 Bad Request response for 
# missing or invalid fields in the request body.
# For example, if total_inventory is missing or is not a number
@video_bp.route("/<id>", method=["PUT"])
def update_video(id):
    video = validate_video(id)
    request_body = request.get_json()
    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    video.available_inventory = request_body["available_inventory"]
    return make_response(jsonify(f"Video #{id} successfully updated"))


# DELETE /videos/<id>
# The API should return back detailed errors 
# and a status 404: Not Found if this video does not exist.
@video_bp.route("/<id>", method=["DELETE"])
def delete_video(id):
    video = validate_video(id)
    db.session.delete(video)
    db.session.commit()
    return make_response(jsonify(f"Video #{id} successfully deleted"))
