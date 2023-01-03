from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(5))
    phone_number = db.Column(db.String(20))
    register_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    videos_checked_out_count = db.Column(db.Integer)