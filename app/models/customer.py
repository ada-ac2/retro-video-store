from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import now

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, server_default=now())
    videos_checked_out_count = db.Column(db.Integer, default=0)
    videos = db.relationship("Video", secondary = "rental", back_populates = "customers")

    def to_dict(self): 
        return {
                "id" : self.id,
                "name": self.name,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "register_at": self.register_at, 
                "videos_checked_out_count":self.videos_checked_out_count
        }



