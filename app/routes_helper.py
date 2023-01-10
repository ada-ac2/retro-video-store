from flask import abort, make_response
from app.models.rental import Rental

# helper function to check model_id
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)
    
    if model:
        return model
        
    abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))


"""# returns tuple containing status of rental and rental count
def get_rental_count(customer_id, video_id):
    rentals = Rental.query.all()
    rental_count = 0
    rental_found = False
    for rental in rentals:
        if rental.customer_id == customer_id:
            if rental.video_id == video_id:
                rental_found = True
                rental_count += 1
    return (rental_count, rental_found)"""