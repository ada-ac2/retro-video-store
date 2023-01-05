from flask import abort, make_response, request

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

    return model


def validate_request_body(cls, request_body):
    if not request_body:
        abourt(make_response({"details":f"Request body is empty."}, 400))

    attributes = cls.__table__.columns.keys()
    attributes.remove("id")
    if "registered_at" in attributes:
        attributes.remove("registered_at")
    if "videos_checked_out_count" in attributes:
        attributes.remove("videos_checked_out_count")
    # check whether there are missing attributes in the request body
    for attribute in attributes:
        if attribute not in request_body.keys():
            abort(make_response({"details":f"Request body must include {attribute}."}, 400))

    # check whether there are extra attributes in the request body
    for attribute in request_body.keys():
        if attribute not in attributes:
            abort(make_response({"details":f"Request body must not include {attribute}."}, 400))

    return request_body