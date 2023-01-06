from app import db

class CustomerRental(db.Model):
    __tablename__ = "customer_rental"
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.id'), primary_key=True,nullable=False)
