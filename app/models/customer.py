from datetime import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        """
        Returns dictionary of customer data.
        """
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
        }
        
    def update_attr(self, attr, val):
        """
        Updates an attr given a *modifiable attr and value. 
        * modifiable attrs: name, postal_code, phone
        """
        if attr == "name":
            self.name = val
        elif attr == "postal_code":
            self.postal_code = val
        elif attr == "phone":
            self.phone = val
        else:
            return False
        return True
    
    def retrieve_by_id(customer_id):
        """
        Returns customer instance given customer id.
        """
        return Customer.query.get(customer_id)
    
    def create_from_dict(dict):
        """
        Creates customer instance from dict values.
        """
        return Customer(
            name=dict["name"],
            postal_code=dict["postal_code"],
            phone=dict["phone"]
        )
