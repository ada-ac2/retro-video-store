from app import db
from sqlalchemy.orm import relationship
from datetime import timedelta
from app.models.video import Video

class Rental(db.Model):
    __tablename__ = "customer_video"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = relationship("Customer", back_populates="rentals")
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    video = relationship("Video", back_populates="rentals")
    due_date = db.Column(db.DateTime(timezone=True), default=db.func.now() + timedelta(days=7), nullable=False)

    def to_dict(self):
        video = Video.get_video_by_id(self.video_id)
        return {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": self.due_date,
            "id": self.id,
            "total_inventory": video.total_inventory
        }

    # @classmethod
    # def from_dict(cls, rental_data):
    #     new_rental = Rental(name=customer_data["name"],
    #     postal_code = customer_data["postal_code"],
    #     phone = customer_data["phone"])
    #     return new_rental