from app import db

def mydefault(context):
    return context.get_current_parameters()['total_inventory']


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    total_inventory = db.Column(db.Integer, default=0, nullable=False)
    available_inventory = db.Column(db.Integer, default=mydefault)
    # long_name = Column(String, unique=True, default=mydefault)

    customers = db.relationship("Rental")
    
    def to_dict(self):
        video_as_dict = dict()
        video_as_dict["id"] = self.id
        video_as_dict["title"] = self.title
        video_as_dict["release_date"] = self.release_date
        video_as_dict["total_inventory"] = self.total_inventory
        video_as_dict["available_inventory"] = self.available_inventory
        return video_as_dict
    
    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(
            title=video_data["title"],
            release_date=video_data["release_date"],
            total_inventory = video_data["total_inventory"],
            # available_inventory = video_data["total_inventory"]
        )
        return new_video