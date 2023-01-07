from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    #__tablename__ = 'rental_table'
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime) 

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customers = db.relationship("Customer", back_populates="videos")
    
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    videos = db.relationship("Video", back_populates="customers")

    def to_dict(self):
        rental_as_dict = {}
        rental_as_dict["id"] = int(self.id)
        rental_as_dict["customer_id"] = self.customer_id
        rental_as_dict["video_id"] = self.video_id
        rental_as_dict["due_date"] = self.due_date

        return rental_as_dict

    @classmethod
    def from_dict(cls, rental_data):
        new_video = Rental(
            due_date=rental_data["due_date"]
        )
        return new_video