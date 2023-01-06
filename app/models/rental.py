from app import db
from app.models.customer import Customer
from app.models.video import Video

class Rental():
    __tablename__ = 'rental'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key = True, nullable = False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key = True, nullable = False)
    due_date = db.Column(db.Date, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", back_populates="video")
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    video = db.relationship("Video", back_populates="customer")

    def to_dict(self):
        rental_as_dict = {}
        rental_as_dict["id"] = int(self.id)
        rental_as_dict["customer_id"] = self.customer_id
        rental_as_dict["video_id"] = self.video_id
        rental_as_dict["due_date"] = self.due_date

        return rental_as_dict