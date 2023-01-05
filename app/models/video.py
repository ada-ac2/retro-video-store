from app import db
import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    total_inventory = db.Column(db.Integer, nullable=False)

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