from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

rentals_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")

