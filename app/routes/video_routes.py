from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, make_response, request, abort


video_bp = Blueprint("video", __name__, url_prefix="/videos")


def validate_video(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))
    return model


def validate_record(video):
    invalid_dict = dict()
    if "title" not in video or not isinstance(video["title"], str) or video["title"] is None:
        invalid_dict["details"] = "Request body must include title."
    if "release_date" not in video or not isinstance(video["release_date"], str) \
        or video["release_date"] is None:
        invalid_dict["details"] = "Request body must include release_date."
    if "total_inventory" not in video or not isinstance(video["total_inventory"], int) \
        or video["total_inventory"] < 0:
        invalid_dict["details"] = "Request body must include total_inventory."
    return invalid_dict

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
    video = validate_video(Video, id)
    return video.to_dict()


# POST /videos
# The API should return back detailed errors and 
# a status 400: Bad Request if the video does not have any of 
# the required fields to be valid.
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    check_invalid_record = validate_record(request_body)
    if check_invalid_record:
        return abort(make_response(jsonify(check_invalid_record), 400))

    new_video = Video.from_dict(request_body)
    
    db.session.add(new_video)
    db.session.commit()
    db.session.refresh(new_video)
    return make_response(jsonify(f"Video {new_video.title} successfully created"), 201)


# PUT /videos/<id>
# The API should return back detailed errors and 
# a status 404: Not Found if this video does not exist.
# The API should return back a 400 Bad Request response for 
# missing or invalid fields in the request body.
# For example, if total_inventory is missing or is not a number
@video_bp.route("/<id>", methods=["PUT"])
def update_video(id):
    video = validate_video(Video, id)
    request_body = request.get_json()
    check_invalid_record = validate_record(request_body)
    if check_invalid_record:
        return abort(make_response(jsonify(check_invalid_record), 400))
    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    #video.available_inventory = request_body["available_inventory"]
    return make_response(jsonify(f"Video #{id} successfully updated"))


# DELETE /videos/<id>
# The API should return back detailed errors 
# and a status 404: Not Found if this video does not exist.
@video_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    video = validate_video(Video, id)
    db.session.delete(video)
    db.session.commit()
    return make_response(jsonify(f"Video #{id} successfully deleted"))
