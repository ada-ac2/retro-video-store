from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    registered_at = db.Column(db.DateTime(timezone = True), nullable = False)
    postal_code = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    videos_checked_out_count = db.Column(db.Integer, default = 0, nullable = False)

# server_default=func.now())