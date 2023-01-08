import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String,nullable = False)
    registered_at = db.Column(db.DateTime,default=(datetime.date.today()))
    postal_code = db.Column(db.String)
    phone = db.Column(db.String,nullable = False)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rentals = db.relationship("Rental", back_populates="customer")



    def to_dict(self):
        customer_dict = {}
        customer_dict["id"] = self.id
        customer_dict["name"] = self.name
        customer_dict["registered_at"] = self.registered_at
        customer_dict["phone"] = self.phone
        customer_dict["postal_code"] = self.postal_code
        return customer_dict

    @classmethod
    def from_dict(cls, customer_data):
        new_customer = Customer(name=customer_data["name"],
                                phone=customer_data["phone"],
                                postal_code = customer_data["postal_code"]
                                )
        return new_customer