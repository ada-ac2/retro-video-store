from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    postal_code = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    videos_checked_out_count = db.Column(db.Integer)