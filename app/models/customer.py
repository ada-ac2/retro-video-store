from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable = False)
    registered_at = db.Column(db.DateTime(timezone = True))
    postal_code = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    videos_checked_in_count = db.Column(db.Integer, default=0)
    videos = db.relationship("Rental")
    
    def to_dict(self):
        customer_as_dict = {}
        customer_as_dict["id"] = int(self.id)
        customer_as_dict["name"] = self.name
        customer_as_dict["postal_code"] = self.postal_code
        customer_as_dict["phone"] = self.phone
        customer_as_dict["registered_at"] = self.registered_at
        customer_as_dict["videos_checked_out_count"] = self.videos_checked_out_count
        return customer_as_dict

    @classmethod
    def from_dict(cls, customer_data):
        new_customer = Customer(name=customer_data["name"],
                        postal_code=customer_data["postal_code"],
                        phone=customer_data["phone"],
                        videos_checked_out_count=customer_data["videos_checked_out_count"]
                        )
        return new_customer
