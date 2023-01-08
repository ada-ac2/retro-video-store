from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, default=0)
    customer = db.relationship("Customer", secondary="rental", backref="video")

    @classmethod
    def get_id(cls, id):
        return Video.query.get(id)