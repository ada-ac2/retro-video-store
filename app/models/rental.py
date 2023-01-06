from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime, default=datetime.utcnow()+timedelta(days=7))
    customers = db.relationship("Customer", back_populates="rentals")
    videos = db.relationship("Video", back_populates="rentals")
