from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=(datetime.date.today()))
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rentals = db.relationship("Rental", back_populates="customer")

    def to_dict(self):
        return {
                "id": self.id,
                "name": self.name,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "registered_at": self.registered_at
            }

    @classmethod
    def from_dict(cls, customer_data):
        new_customer = Customer(name = customer_data["name"],
                    postal_code = customer_data["postal_code"],
                    phone = customer_data["phone"],
                    registered_at = customer_data["registered_at"]
                    )
        return new_customer
