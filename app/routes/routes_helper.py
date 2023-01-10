from flask import abort, make_response

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    
    return model

    #  return True if its a valid number, return False it's not a number
def validate_num_queries(query_param):
    try:
        query_int = int(query_param)
    except:
        return False
    return True