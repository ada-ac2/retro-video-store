from app import db
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request 
from datetime import datetime

rentals_bp = Blueprint("rentals_bp",__name__, url_prefix="/rentals")