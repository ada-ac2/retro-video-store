from app import db
import datetime as dt
from .video import Video
from .customer import Customer

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.relationship("Customer", back_populates="rentals")
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    video = db.relationship("Video", back_populates="rentals")
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    due_date = db.Column(db.DateTime, default=dt.datetime.now()+dt.timedelta(days=7))
    status = db.Column(db.String(), default="checked_out")
    n_video_copies = db.Column(db.Integer, default=1)

    def to_dict(self):
        """
        Returns dictionary of rental data and *customer/video data if exists
        """
        rental_dict = {
            "id": self.id,
            "due_date": self.due_date,
            "n_video_copies": self.n_video_copies,
            "status": self.status
        }
        if self.customer:
            customer_dict = self.customer.to_dict()
            customer_dict["customer_id"] = customer_dict.pop("id")
            rental_dict.update(customer_dict)
        if self.video:
            video_dict = self.video.to_dict()
            video_dict["video_id"] = video_dict.pop("id")
            rental_dict.update(video_dict)
        return rental_dict
    
    @classmethod
    def from_dict(cls, rental_data):
        new_rental = Rental(
            customer_id=rental_data["customer_id"],
            video_id=rental_data["video_id"]
        )
        return new_rental

    @classmethod
    def get_all_attrs(cls):
        """
        Returns list of attributes for Rental class
        """
        return ["name", "postal_code", "registered_at", "title", "release_date"]