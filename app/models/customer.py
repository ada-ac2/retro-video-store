from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.datetime.now().strftime("%a, %d %b %Y %X %z"))
    videos_checked_out_count = db.Column(db.Integer, nullable=False, default=0)
    videos = db.relationship("Video", secondary="rental", back_populates="customers")

    def to_dict(self):
        customer_dict = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return customer_dict