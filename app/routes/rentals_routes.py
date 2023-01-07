from app import db
from flask import Blueprint, jsonify, make_response, abort, request
from ..models.rental import Rental

# ~~~~~~ initialize rentals blueprint ~~~~~~
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")