from app import db
from app.models.video import Video
from app.models.customer import Customer
from sqlalchemy import func
from datetime import timedelta
from .video import Video
from .customer import Customer
from datetime import datetime, timedelta, date

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.Date, nullable=True)
    #is_checked_out = db.Column(db.Boolean, default=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

'''
    @staticmethod
    def due_date():
        due_date = datetime.today() + timedelta(days=7)
        return due_date
'''
