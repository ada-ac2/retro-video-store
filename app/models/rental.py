from app import db

class Rental():
    __tablename__ = 'rental'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key = True, nullable = False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key = True, nullable = False)
    due_date = db.Column(db.Date, nullable = False)

    #customer = db.relationship("Customer", back_populates="videos")
    #video = db.relationship("Video", back_populates="customers")

