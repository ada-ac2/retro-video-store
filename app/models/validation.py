from flask import make_response, abort, request
from app.models.rental import Rental


# ~~~~~~ validation checkers and processing functions ~~~~~~
def validate_model(cls, model_id):
    """
    Checks if model id is correct dtype (int) and if exists in db.
    :params:
    - model_id
    :returns:
    - response_msg (dict), status_code (int)
    """
    # check if model id is integer dtype
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} should be an integer dtype"}, 400))
    # fetch model by id
    model = cls.query.get(model_id)
    if not model:
        return abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))
    else:
        return model

def validate_request(request, reqs):
    """
    Validates that http requests satisfy all requirements for PUT methods
    :params:
    - request (from client)
    :returns:
    - request_body (if requirements met)
    """
    
    # collect request
    request_body = request.get_json()
    # check if all requirements in request
    set_request_keys = set(request_body.keys())
    set_reqs= set(reqs)
    if not set_request_keys == set_reqs:
        missing_key = "".join(set_reqs-set_request_keys)
        return abort(make_response({
                "details": f"Request body must include {missing_key}."
        }, 400))
    return request_body

def validate_and_process_query_params(cls, queries):
    """
    Parse query parameters from HTTP request and separate into separate dictionaries 
    based on SQLAlchemy query method
    :params:
    - cls (class)
    - queries (dict)
    :returns:
    - sort (dict): query params for order_by sorting method (ascending)
    - count (dict): selected number of results for limit method
    - page_num (dict): page
    """
    attrs = cls.get_all_attrs()
    sort = None
    count = None
    page_num = None
    for kwarg in queries:
        # check for sort method query param
        if kwarg == "sort":
            # if sort string is not a model attribute
            if queries[kwarg] in attrs:
                sort = queries[kwarg]
        # check for limit method query param
        if kwarg == "count":
            # add count to count kwarg dict
            try:
                count = int(queries[kwarg])
            except ValueError:
                pass
        # check for page count method query param
        if kwarg == "page_num":
            try:
                page_num = int(queries[kwarg])
            except ValueError:
                pass
    return sort, count, page_num

def create_model_query(models_query, cls, sort, count, page_num):
    if sort:
        # sort asc by given attribute e.g. sort=name
        clause = getattr(cls, sort["sort"])
        model_query = models_query.order_by(clause.asc())
    # else:
    #     models = models.order_by(cls.id.asc())
    if count:
        # limit selection of customers to view
        models_query = models_query.limit(count["count"])
    if page_num:
        # check documentation for this!!!
        pass
    return models_query