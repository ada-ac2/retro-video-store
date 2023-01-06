from app import db
from datetime import datetime, timedelta

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.utcnow())
    total_inventory = db.Column(db.Integer, nullable=False)
    rentals = db.relationship("Rental", secondary="video_rental", back_populates="videos")
    # video_rentals = db.relationship("Rental", back_populates="video_rental")

    def to_dict(self):
        
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
        )
        return new_obj