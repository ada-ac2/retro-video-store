from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)

    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(title = video_data["title"],
                        release_date=video_data["release_date"],
                        total_inventory = video_data['total_inventory'])
        return video_data
#     {
#   "id": 1,
#   "title": "Blacksmith Of The Banished",
#   "release_date": "1979-01-18",
#   "total_inventory": 10
# }