from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postal_code = db.Column(db.String(5), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    register_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    videos_checked_out_count = db.Column(db.Integer)