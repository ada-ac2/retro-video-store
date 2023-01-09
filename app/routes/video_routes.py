from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.validation import validate_model, validate_request, validate_and_process_query_params, create_model_query
from flask import Blueprint, jsonify, make_response, request

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")

@video_bp.route("", methods=["GET"])
def get_all_videos():
    request_query = request.args.to_dict()
    # collect & process query params from http request
    sort, count, page_num = validate_and_process_query_params(Video, request_query)
    # create query
    videos = Video.query
    videos = create_model_query(videos, Video, sort, count, page_num)
    # fill http response list
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return make_response(jsonify(videos_response), 200)

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
    # collect & process query params from http request
    #queries = request.args.to_dict()
    #sort, count, page_num = validate_and_process_query_params(Rental, queries)
    # collect rentals using query params
    request_query = request.args.to_dict()
    sort, count, page_num = validate_and_process_query_params(Rental, request_query)
    # collect rentals by customer id
    rental_query = Rental.query.filter_by(video_id = video.id)
    # default is sorted by asc rental id
    rentals = rental_query.order_by(Rental.id.asc())
    if count:
        # limit selection of customers to view
        rentals = rental_query.limit(count["count"])
    #rentals = create_model_query(video, Video, sort, count, page_num)
    rentals_response = []
    for rental in video.rentals:
        rentals_response.append(rental.to_dict())
        print(rental.to_dict())
    return make_response(jsonify(rentals_response), 200)

