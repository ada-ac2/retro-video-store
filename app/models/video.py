from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String,nullable = False)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)


    def to_dict(self):
        video_dict = {}
        video_dict["title"] = self.id
        video_dict["release_date"] = self.release_date
        video_dict["total_inventory"] = self.total_inventory
        
        return video_dict