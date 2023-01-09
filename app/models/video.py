from app import db

def mydefault(context):
        return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    release_date = db.Column(db.Date())
    total_inventory = db.Column(db.Integer())
    available_inventory = db.Column(db.Integer(),default=mydefault)
    rentals = db.relationship("Rental", back_populates="video")

    def to_dict(self):
        """
        Returns dictionary of video data
        """
        video_dict = {
                "id": self.id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory,
                "available_inventory": self.available_inventory,
                }
        return video_dict

    def calculate_available_inventory(self):
        """
        Calculate number of available videos to rent
        """
        self.available_inventory = self.total_inventory - self.rentals.n_video_copies

    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(
            title=video_data["title"],
            release_date=video_data["release_date"],
            total_inventory=video_data["total_inventory"]
                        )
        return new_video
    
    @classmethod
    def get_all_attrs(cls):
        """
        Returns list of attributes for Video class
        """
        return ["title", "release_date"]

