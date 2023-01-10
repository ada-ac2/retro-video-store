from flask import abort, make_response,jsonify

def validate_model(model, id):
    try:
        int(id)
    except:
        abort(make_response({"message": f"{id} is an invalid {model.__name__} id"}, 400))

    model_instance = model.query.get(id)

    if not model_instance:
        abort(make_response({"message": f"{model.__name__} {id} was not found"}, 404))
    
    return model_instance

def validate_request_body(request_body,required_data):
    if not request_body:
        msg = "An empty or invalid json object was sent."
        abort(make_response(jsonify({"details":msg}),400))

    for data in required_data:
        if data not in request_body: 
            msg = f"Request body must include {data}. Request failed"
            abort(make_response(jsonify({"details":msg}),400))

