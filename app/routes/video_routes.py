from flask import Blueprint, jsonify, abort, make_response,request
from app.models.video import Video
from app import db

videos_bp = Blueprint("videos_bp",__name__, url_prefix="/videos")

@videos_bp.route("",methods=["GET"])
def get_all_videos():
    videos_query = Video.query

    videos = videos_query.all()
    videos_response = [video.to_dict() for video in videos]

    return jsonify(videos_response)

def validate_video_id(video_id):
    try:
        id = int(video_id)
    except:
        msg = f"Video id: {video_id} is Invalid"
        abort(make_response(jsonify({"message": msg}),400))

    video = Video.query.get(id)

    if video:
        return video

    msg = f"Video {video_id} was not found"
    abort(make_response(jsonify({"message": msg}),404))

@videos_bp.route("/<video_id>",methods=["GET"])
def get_video(video_id):
    video = validate_video_id(video_id)
    return jsonify(video.to_dict())  

@videos_bp.route("",methods=["POST"])
def create_video():
    request_body = request.get_json(silent=True)
    if not request_body:
        msg = "An empty or invalid json object was sent. Can't create video"
        abort(make_response(jsonify({"message":msg}),400))

   
    req_title = request_body.get("title")
    req_total_inventory = request_body.get("total_inventory")
    req_release_date = request_body.get("release_date") 

    if not req_title:
        msg = "Request body must include title. Can't create video"
        abort(make_response(jsonify({"details":msg}),400))

    if not req_total_inventory:
        msg = "Request body must include total_inventory. Can't create video"
        abort(make_response(jsonify({"details":msg}),400))

    if not req_release_date:
        msg = "Request body must include release_date. Can't create video"
        abort(make_response(jsonify({"details":msg}),400))

    new_video = Video(
            title = req_title,
            total_inventory = req_total_inventory,
            release_date = req_release_date
    )

    try:
        db.session.add(new_video)
        db.session.commit()

    except:
        msg = "Error creating video in db"
        abort(make_response(jsonify({"message":msg}),500))

    return make_response(jsonify(new_video.to_dict()),201)
