from datetime import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.now())
    rentals = db.relationship("Rental", back_populates="customer")
    videos_checked_out_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        """
        Returns dictionary of customer data.
        """
        customer_dict = {
                "id": self.id,
                "name": self.name,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "registered_at": self.registered_at,
                "videos_checked_out_count": self.videos_checked_out_count,
        }
        return customer_dict

    def check_out_videos(self, n):
        self.n_rented_videos += n
        
    def check_in_videos(self, n):
        self.n_rented_videos -= n
    
    @classmethod
    def create_from_dict(cls, dict):
        """
        Creates customer instance from dict values.
        """
        return Customer(
            name=dict["name"],
            postal_code=dict["postal_code"],
            phone=dict["phone"]
        )

    @classmethod
    def get_all_attrs(cls):
        """
        Returns list of attributes for Customer class
        """
        return ["name", "postal_code", "phone", "registered_at"]