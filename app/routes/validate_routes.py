from flask import Blueprint, jsonify, abort, make_response, request

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

# Validate post rentals/check_in 
# Required Request Body Parameters: customer_id, video_id
# Return 404: Not Found if eather not exist
# Return 400: Bad Request if the video and customer do not match 
# a current rental

# Add check available_inventory function
# require video_id parameter
# return available numbers of copy 
