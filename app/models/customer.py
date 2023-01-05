from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    #videos_checked_out_count = db.Column(db.Integer)
    #def to_dict(self):
        


    @classmethod
    def from_dict(cls, customer_data):
        new_customer = Customer(name = customer_data["name"],
                        registered_at=customer_data["registered_at"],
                        postal_code = customer_data['postal_code'],
                        phone = customer_data['phone'])
        return customer_data


# #  {
#     "id": 1,
#     "name": "Shelley Rocha",
#     "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
#     "postal_code": "24309",
#     "phone": "(322) 510-8695"
#   },