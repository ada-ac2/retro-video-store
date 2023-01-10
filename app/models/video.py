from app import db


def available_inventory_default(context):
    return context.get_current_parameters()['total_inventory']
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    available_inventory = db.Column(db.Integer, default=available_inventory_default)
    release_date = db.Column(db.DateTime, nullable=False)
    customers = db.relationship("Customer",secondary="rental",back_populates="videos")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory,
            "release_date": self.release_date
        }
    
