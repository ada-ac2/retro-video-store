from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import now

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        customer_as_dict = {}
        customer_as_dict["id"] = self.id
        customer_as_dict["name"] = self.name
        #customer_as_dict["registered_at"] = self.registered_at
        customer_as_dict["postal_code"] = self.postal_code
        customer_as_dict["phone"] = self.phone        

        return customer_as_dict

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