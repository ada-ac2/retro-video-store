from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    videos_checked_out_count = db.Column(db.Integer)
    rentals = db.relationship("Rental", back_populates="video")

    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory

            }

    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(title=video_data["title"],
                    release_date=video_data["release_date"],
                    total_inventory=video_data["total_inventory"]
                            )
        return new_video