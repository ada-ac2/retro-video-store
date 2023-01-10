from app import db
import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, default=datetime.date.today())
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=0)
    customers = db.relationship("Customer", secondary="rental", back_populates="videos")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            "total_inventory": self.total_inventory
        }
    
    @classmethod
    def from_dict(cls, data):
        pass