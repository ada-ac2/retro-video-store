from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime

class Rental():
    __tablename__ = 'rentals'
    #id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable = False)   
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key = True, nullable = False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key = True, nullable = False)
    customer = db.relationship("Customer", back_populates="videos")
    videos = db.relationship("Video", back_populates="customers")

    def to_dict(self):
        rental_as_dict = {}
        #rental_as_dict["id"] = int(self.id)
        rental_as_dict["customer_id"] = self.customer_id
        rental_as_dict["video_id"] = self.video_id
        rental_as_dict["due_date"] = self.due_date

        return rental_as_dict