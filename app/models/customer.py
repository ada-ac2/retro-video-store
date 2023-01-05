from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    videos_checked_out_count = db.Column(db.Integer)