from app import db
from datetime import date, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    due_date = db.Column(db.Date, default = date.today() + timedelta(days=7))
    videos_checked_out_count = db.Column(db.Integer) 
    available_inventory = db.Column(db.Integer) 
    checked_in = db.Column(db.Boolean, default = False)
    checkout_date = db.Column(db.Date, default = date.today())

    def to_dict(self):
        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "due_date" : self.due_date, 
            "videos_checked_out_count" : self.videos_checked_out_count,
            "available_inventory" : self.available_inventory, 
            "checked_in" : self.checked_in 
        }
