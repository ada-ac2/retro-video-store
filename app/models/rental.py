from app import db
import datetime

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    due_date = db.Column(db.DateTime, default=(datetime.date.today()+datetime.timedelta(days=7)))
    check_out_status = db.Column(db.Boolean,default = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'),nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'),nullable=False)
    customer = db.relationship("Customer", back_populates="rentals")
    video = db.relationship("Video", back_populates="rentals")

    def to_dict(self):
        rental_dict = {}
        rental_dict["id"] = self.id
        rental_dict["customer_id"] = self.customer_id
        rental_dict["video_id"] = self.video_id
        rental_dict["due_date"] = self.due_date
        rental_dict["check_out_status"] = self.check_out_status
        return rental_dict

    @classmethod
    def from_dict(cls, rental_data):
        new_rental = Rental(
            customer_id = rental_data["customer_id"],
            video_id = rental_data["video_id"]
        )
        return new_rental


