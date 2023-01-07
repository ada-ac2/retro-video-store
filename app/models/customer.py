from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import now

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, server_default = now())
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default = 0)
    rentals = db.relationship('Rental', back_populates='customer')
        
    def to_dict(self):
        customer_as_dict = {}
        customer_as_dict["id"] = self.id
        customer_as_dict["name"] = self.name
        #customer_as_dict["registered_at"] = self.registered_at
        customer_as_dict["postal_code"] = self.postal_code
        customer_as_dict["phone"] = self.phone        

        return customer_as_dict

    def to_json(self):
        return {
        "id": self.id,
        "name": self.name,
        "phone": self.phone,
        "postal_code": self.postal_code,
        "videos_checked_out_count": self.videos_checked_out_count,
        "registered_at": self.registered_at
        }



    @classmethod
    def from_dict(cls, customer_data):
        new_customer = Customer(name = customer_data["name"],
                        #registered_at=customer_data["registered_at"],
                        postal_code = customer_data["postal_code"],
                        phone = customer_data["phone"])
        return new_customer

    @classmethod
    def get_id(cls, id):
        return Customer.query.get(id)

    def get_videos_checked_out_count(self):
        num_of_rentals = 0
        for rental in self.rentals:
            if rental.is_checked_out:
                num_of_rentals += 1
        return num_of_rentals
# #  {
#     "id": 1,
#     "name": "Shelley Rocha",
#     "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
#     "postal_code": "24309",
#     "phone": "(322) 510-8695"
#   },