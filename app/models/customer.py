from app import db
from datetime import datetime, timedelta

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow())
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    videos_checked_out_count = db.Column(db.Integer)
    rentals = db.relationship("Rental", back_populates="customer")


    def to_dict(self):
        customer_dict = {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone, 
            "videos_checked_out_count": self.videos_checked_out_count
        }

        video_rentals = []
        for rental in self.rentals:
            video_rentals.append(rental)
        customer_dict["rentals"] = video_rentals

        return customer_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            name = request_body["name"],
            registered_at = request_body["registered_at"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"], 
            videos_checked_out_count = request_body["videos_checked_out_count"]
        )
        return new_obj