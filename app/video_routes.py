from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, abort, make_response, request

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
