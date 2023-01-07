from app import db
from app.models.video import Video
from app.models.customer import Customer
from sqlalchemy import func
from datetime import timedelta
from .video import Video
from .customer import Customer


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    #have the datetimes calcuated by the db server. func.now() tells db to calc the timestamp
    due_date = db.Column(db.DateTime, default=func.now() + timedelta(days=7))
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    is_checked_out = db.Column(db.Boolean, default=True)
    video = db.relationship("Video", back_populates="rentals")
    customer = db.relationship("Customer", back_populates="rentals")
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def to_dict(self):
        rental_dict = {}
        rental_dict["id"] = self.id
        rental_dict["name"] = self.name
        rental_dict["due_date"] = self.due_date
        rental_dict["videos_checked_out_count"] = self.videos_checked_out_count
        rental_dict["available_inventory"] = self.available_inventory

    #@classmethod
    #def from_dict(cls, rental_data):
        #new_rental = Rental(
                        #video_id = rental_data["video_id"],
                        #customer_id = rental_data["customer_id"],
                        #due_date = rental_data["due_date"],
                        # videos_checked_out_count = rental_data['videos_checked_out_count'],
                        #avaliable_inventory = rental_data['avaliable_inventory']
                    # )
        #return new_rental



    def to_json(self):
        video = Video.get_id(self.video_id)
        return {
            "title": video.title,
            "due_date": self.due_date,
            "release_date": video.release_date
        }

    def get_rental_by_video_id(self, id):
        customer = Customer.query.get(id)
        return {
            "name": customer.name,
            "due_date": self.due_date,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }

    def get_rental_by_customer_id(self, id):
        video = Video.query.get(id)
        return {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": self.due_date
        }

    @classmethod
    def check_out(cls, video_id, customer_id):
        new_rental = cls(video_id=video_id, customer_id=customer_id)

        if not new_rental:
            return None

        video = Video.get_id(new_rental.video_id)
        customer = Customer.get_id(new_rental.customer_id)

        db.session.add_all([new_rental, video, customer])
        db.session.commit()

        videos_checked_out_count = customer.get_videos_checked_out_count()
        available_video_inventory = video.get_available_video_inventory()

        return {
            "video_id": new_rental.video_id,
            "customer_id": new_rental.customer_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_video_inventory
        }, 200

    @classmethod
    def check_in(cls, video_id, customer_id):
        print(video_id,customer_id)
        rental_check_in = cls.query.filter(
            Rental.customer_id==customer_id,
            Rental.video_id==video_id,
            Rental.is_checked_out==True
            ).first()
        
        video = Video.get_id(video_id)
        customer = Customer.get_id(customer_id)
        print(rental_check_in)
        if not rental_check_in:
            return {
                "message": f"No outstanding rentals for customer {customer.id} and video {video.id}"
            }, 400
            
        rental_check_in.is_checked_out = False

        db.session.delete(rental_check_in)
        db.session.commit()

        videos_checked_out_count = customer.get_videos_checked_out_count()
        available_video_inventory = video.get_available_video_inventory()

        return {
            "video_id": rental_check_in.video_id,
            "customer_id": rental_check_in.customer_id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_video_inventory
        }, 200

        