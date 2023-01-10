from app import db
from flask import abort, make_response, jsonify
from sqlalchemy.orm import relationship

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    rentals = db.relationship("Rental", back_populates="video")


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    def available_inventory(self):
        return self.total_inventory - len(self.rentals)

    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(title=video_data["title"], release_date=video_data["release_date"], total_inventory=video_data["total_inventory"])
        return new_video

    @classmethod
    def get_video_by_id(cls, video_id):
        return cls.query.get(video_id)