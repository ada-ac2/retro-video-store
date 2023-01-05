from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    due_date = db.Column(db.Datetime)
    videos_checked_out_count = db.Column(db.Integer)
    avaliable_inventory = db.Column(db.Integer)

    @classmethod
    def from_dict(cls, rental_data):
        new_rental = Rental(
                        name = rental_data["name"],
                        due_date=rental_data["due_date"],
                        videos_checked_out_count = rental_data['videos_checked_out_count'],
                        avaliable_inventory = rental_data['avaliable_inventory']
                    )
        return new_rental