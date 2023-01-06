from app import db

class VideoRental(db.Model):
    __tablename__ = "video_rental"
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.id'), primary_key=True,nullable=False)
