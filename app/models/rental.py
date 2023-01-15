from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    #__tablename__ = 'rental_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    due_date = db.Column(db.DateTime, default=datetime.now()+timedelta(days=7), nullable=False)
    status = db.Column(db.String, default="Checked out", nullable=False)

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
            customer_id=rental_data["customer_id"],
            video_id=rental_data["video_id"]
        )
        
        return new_video