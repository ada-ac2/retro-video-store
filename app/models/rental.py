from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime, default=datetime.utcnow()+timedelta(days=7))
    customer = db.relationship("Customer", back_populates="rentals")
    video = db.relationship("Video", back_populates="rentals")

    def to_dict(self):
        rental_dict = {
            "id": self.id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date.strftime("%m-%d-%Y")
        }

        return rental_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            customer_id = request_body["customer_id"],
            video_id = request_body["video_id"]
        )
        return new_obj
