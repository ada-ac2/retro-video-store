from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String,nullable = False)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
