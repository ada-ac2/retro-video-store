# Wave 3: Enhancements & Deployment

## Query Parameters
The following 3 query parameters:

| Name          | Value   | Description
|---------------|---------|------------
| `sort`        | string  | Sort objects by this field, in ascending order
| `count`       | integer | Number of responses to return per page
| `page_num`    | integer | Page of responses to return

should be accepted by the following three endpoints:
- `GET /customers`
- `GET /customers/<id>/rentals`

So, for an API endpoint like `GET /customers`, the following requests should be valid:
- `GET /customers`: All customers, sorted by ID
- `GET /customers?sort=name`: All customers, sorted by name
- `GET /customers?count=10&page_num=2`: Customers 11-20, sorted by ID
- `GET /customers?sort=name&count=10&page_num=2`: Customers 11-20, sorted by name

Things to note:
- All three query parameters are an _optional_ part of the request body
- Possible sort fields:
  - Customers can be sorted by `name`, `registered_at` and `postal_code`
  - Videos can be sorted by `title` and `release_date`
- If the client requests both sorting and pagination, pagination should be relative to the sorted order
  - The paginate method reteurns a [Pagination object](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination)
  - To access records from a Pagination object, consider using the `items` attribute
  - See [this article from DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-query-tables-and-paginate-data-in-flask-sqlalchemy) for a more detailed look at paginating data using SQLAlchemy 


#### Errors and Edge Cases to Check

- The API should default to sorting by `id` if no `sort` parameter is specified
- The API should default to sorting by `id` if a value other than `name`, `registered_at`, or `postal_code` is passed in for the parameter `sort`
- The API should default to returning all customers in a single page if no number of per page responses is specified
- The API should default to returning all customers in a single page if an invalid number of per page responses is specified
- The API should default to returning the first page if no page is specified
- The API should default to returning the first page if an invalid page is specified

## Deployment

Deploy this project to Heroku.

Then, add some Customer, Video, and Rental records to the production database.

Be sure to grab the URL of your deployed app. It will be submitted at the time of project submission.

### Tips
- When unexpected issues come up, employ all of your debugging skills:
  - Write down what step/command created the issue
  - Write down how you observe the issue
  - Attempt to recreate the issue locally
  - Use Postman, the browser, and the debugger tools
  - Use the Heroku logs
  - Research error messages
  - Rubber duck and ask for help in slack


