from app import db
import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, default=datetime.datetime.now())
    videos_checked_out_count = db.Column(db.Integer)
    
    def to_dict(self):
        customer_dict = {}
        customer_dict["id"] = self.id
        customer_dict["name"] = self.name
        customer_dict["postal_code"]=self.postal_code
        customer_dict["phone"] = self.phone
        
        return customer_dict


    @classmethod
    def from_dict(cls,customer_data):
        new_customer = Customer(
            name=customer_data["name"],
            postal_code=customer_data["postal_code"],
            phone=customer_data["phone"],
        )
        return new_customer