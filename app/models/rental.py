from app import db
import datetime as dt

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.relationship("Customer", back_populates="rentals")
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    video = db.relationship("Video", back_populates="rentals")
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    due_date = db.Column(db.DateTime, default=dt.datetime.now()+dt.timedelta(days=7))
    status = db.Column(db.String(), default="checked_out")
    n_video_copies = db.Column(db.Integer, default=1)

    def to_dict(self):
        """
        Returns dictionary of rental data and customer data if customer
        """
        rental_dict = {
                "due_date": self.due_date,
                "n_video_copies": self.n_video_copies,
        }
        if self.customer:
            rental_dict.update(self.customer.to_dict())
        if self.video:
            rental_dict.update(self.video.to_dict())
        return rental_dict
    
    @classmethod
    def from_dict(cls, rental_data):
        new_rental = Rental(
            customer_id=rental_data["customer_id"],
            video_id=rental_data["video_id"]
        )
        return new_rental

    # def check_out_video(self, n):
    #     """
    #     Updates video available inventory when customer checks out video(s)
    #     """
    #     # decrement the video inventory
    #     self.video.calculate_available_inventory()
    #     # increment the customer's number of rented videos
    #     self.customer.check_out_videos(n)

    # def check_in_video(self):
    #     """
    #     Updates video available inventory when customer checks out video(s)
    #     """
    #     # decrement the video inventory
    #     self.video.calculate_available_inventory()
    #     # increment the customer's number of rented videos
    #     self.customer.check_out_videos()

    # def check_in_video(self, n):
    #     """
    #     Updates videos checked out count and video available inventory
    #     :params:
    #     - n: number of videos to check in
    #     """
    #     self.num_duplicates_video -= n
    #     self.video.calculate_available_inventory()

    