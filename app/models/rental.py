from app import db

class Rental():
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.Date, nullable = False)

    customer = db.relationship("Customer", back_populates="videos")
    video = db.relationship("Video", back_populates="customers")

