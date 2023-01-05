from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, default=datetime.utcnow()+timedelta(days=3))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer_rental = db.relationship("Customer", back_populates="rentals")
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video_rental = db.relationship("Video", back_populates="rentals")
