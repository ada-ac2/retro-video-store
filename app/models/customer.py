from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import now

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    @classmethod
    def get_id(cls, id):
        return Customer.query.get(id)