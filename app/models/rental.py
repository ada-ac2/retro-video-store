from app import db
import datetime
import enum
from sqlalchemy import Enum


class Rental(db.Model):

    class RentalStatus(enum.Enum):
        CHECKIN="checked_in"
        CHECKOUT="checked_out"
    

    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    status = db.Column(db.Enum(RentalStatus), default=RentalStatus.CHECKOUT)
    checkout_date = db.Column(db.DateTime, default=datetime.datetime.now())
    due_date = db.Column(db.DateTime, default=(datetime.date.today()+datetime.timedelta(days=7)))
