from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    release_date = db.Column(db.Date, nullable = False)
    total_inventory = db.Column(db.Integer, default = 0, nullable = False)
    available_inventory = db.Column(db.Integer, default = 0, nullable = False)