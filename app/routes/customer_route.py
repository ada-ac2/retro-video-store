from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request 

customers_bp = Blueprint("customers_bp",__name__, url_prefix="/customers")