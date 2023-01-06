from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from .validate_routes import validate_model, validate_customer_user_input
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

# Routes:

#POST /rentals/check-out

#POST /rentals/check-in

