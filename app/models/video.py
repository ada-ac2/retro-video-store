from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer)