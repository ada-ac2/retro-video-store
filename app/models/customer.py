from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)
    # videos_checked_out = db.Column(db.Integer)

    def to_dict(self):
        """
        Returns dictionary of customer data.
        """
        return {
            "id": self.id,
            "name": self.name,
            "postal code": self.postal_code,
            "phone number": self.phone_number,
            "registered at": self.registered_at,
        }