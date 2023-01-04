from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        video_dict = {}
        video_dict["id"] = self.id
        video_dict["title"] = self.title
        video_dict["release_date"] = self.release_date
        video_dict["total_inventory"] = self.total_inventory

        return video_dict

    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(
            title=video_data["title"], 
            release_date=video_data["release_date"],
            total_inventory=video_data["total_inventory"]
        )
        
        return new_video