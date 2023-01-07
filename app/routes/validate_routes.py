from flask import abort, make_response
from app.models.video import Video
import datetime

# Validating the id of the customer: id needs to be int and exists the planet with the id.
# Returning the valid class instance if valid id
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    class_obj = cls.query.get(model_id)
    if not class_obj:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

    return class_obj

# Validating the user input to create or update the customer
# Returning the valid JSON if valid input
def validate_customer_user_input(customer_value):
    invalid_dict = {}
    if "name" not in customer_value \
        or not isinstance(customer_value["name"], str) \
        or customer_value["name"] == "":
        invalid_dict["details"] = "Request body must include name."
    if "postal_code" not in customer_value \
        or not isinstance(customer_value["postal_code"], str) \
        or customer_value["postal_code"] == "":
        invalid_dict["details"] = "Request body must include postal_code."
    if "phone" not in customer_value \
        or not isinstance(customer_value["phone"], str) \
        or customer_value["phone"] == "":
        invalid_dict["details"] = "Request body must include phone."

    return invalid_dict

def validate_record(video):
    invalid_dict = dict()
    if "title" not in video or not isinstance(video["title"], str) or video["title"] is None:
        invalid_dict["details"] = "Request body must include title."
    if "release_date" not in video or not isinstance(video["release_date"], str) \
        or video["release_date"] is None:
        invalid_dict["details"] = "Request body must include release_date."
    if "total_inventory" not in video or not isinstance(video["total_inventory"], int) \
        or video["total_inventory"] < 0:
        invalid_dict["details"] = "Request body must include total_inventory."
    return invalid_dict

# Validate post rentals/check_out 
# Required Request Body Parameters: customer_id, video_id
# Return 404: Not Found if eather not exist
# Return 400: Bad Request if the video does not have any available 
# inventory before check out
def validate_rental_out(rental_out):
    invalid_dict = dict()
    if "customer_id" not in rental_out or not isinstance(rental_out["customer_id"], int) or \
        rental_out["customer_id"] is None:
        invalid_dict["detail"] = "Request body must include customer_id."
    if "video_id" not in rental_out or not isinstance(rental_out["video_id"], int) or \
        rental_out["video_id"] is None:
        invalid_dict["detail"] = "Request body must include video_id."
    return invalid_dict


# Validate post rentals/check_in 
# Required Request Body Parameters: customer_id, video_id
# Return 404: Not Found if eather not exist
# Return 400: Bad Request if the video and customer do not match 
# a current rental
def validate_rental_in(rental_in):
    invalid_dict = dict()
    if "customer_id" not in rental_in or not isinstance(rental_in["customer_id"], int) or \
        rental_in["customer_id"] is None:
        invalid_dict["detail"] = "Request body must include customer_id."
    if "video_id" not in rental_in or not isinstance(rental_in["video_id"], int) or \
        rental_in["video_id"] is None:
        invalid_dict["detail"] = "Request body must include video_id."
    return invalid_dict

# Add check available_inventory function
# require video_id parameter
# return available numbers of copy 
def check_inventory(video):
    invalid_dict = dict()
    if video.available_inventory < 1:
        invalid_dict["message"] = "Could not perform checkout"
    return invalid_dict

def check_due_date(rental):
    invalid_dict = dict()
    if rental.due_date < datetime.now():
        invalid_dict["message"] = "Passed due date"
    return invalid_dict

def check_outstanding_videos(video, customer):
    invalid_dict = {"message" : f"No outstanding rentals for customer {customer.id} and video {video.id}"}
    available_videos = Video.query.all()
    for available_video in available_videos:
        if available_video.id == video.id and video.available_inventory < video.total_inventory:
            invalid_dict = {}
            break
    return invalid_dict