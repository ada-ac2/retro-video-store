from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String) 
    phone = db.Column(db.String) 
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)


