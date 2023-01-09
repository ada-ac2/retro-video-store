from app.models.video import Video
from app.models.customer import Customer

VIDEO_1_TITLE = "A Brand New Video"
VIDEO_1_ID = 1
VIDEO_1_INVENTORY = 1
VIDEO_1_RELEASE_DATE = "01-01-2001"

VIDEO_2_TITLE = "Video Two"
VIDEO_2_ID = 2
VIDEO_2_INVENTORY = 1
VIDEO_2_RELEASE_DATE = "12-31-2000"

VIDEO_3_TITLE = "Video Three"
VIDEO_3_ID = 3
VIDEO_3_INVENTORY = 1
VIDEO_3_RELEASE_DATE = "01-02-2001"

CUSTOMER_1_NAME = "A Brand New Customer"
CUSTOMER_1_ID = 1
CUSTOMER_1_POSTAL_CODE = "12345"
CUSTOMER_1_PHONE = "123-123-1234"

CUSTOMER_2_NAME = "Second Customer"
CUSTOMER_2_ID = 2
CUSTOMER_2_POSTAL_CODE = "12345"
CUSTOMER_2_PHONE = "234-234-2345"

CUSTOMER_3_NAME = "Customer Three"
CUSTOMER_3_ID = 3
CUSTOMER_3_POSTAL_CODE = "12344"
CUSTOMER_3_PHONE = "000-000-0000"


def test_get_customers_no_query_params_sorts_by_id(client, one_customer, second_customer, third_customer):
    # Act
    response = client.get("/customers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

    assert response_body[2]["name"] == CUSTOMER_3_NAME
    assert response_body[2]["id"] == CUSTOMER_3_ID
    assert response_body[2]["phone"] == CUSTOMER_3_PHONE
    assert response_body[2]["postal_code"] == CUSTOMER_3_POSTAL_CODE

def test_get_customers_sorted_by_name(client, one_customer, second_customer, third_customer):
    # Arrange
    data = {"sort": "name"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_3_NAME
    assert response_body[1]["id"] == CUSTOMER_3_ID
    assert response_body[1]["phone"] == CUSTOMER_3_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_3_POSTAL_CODE

    assert response_body[2]["name"] == CUSTOMER_2_NAME
    assert response_body[2]["id"] == CUSTOMER_2_ID
    assert response_body[2]["phone"] == CUSTOMER_2_PHONE
    assert response_body[2]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_customers_sorted_by_postal_code(client, one_customer, second_customer, third_customer):
    # Arrange
    data = {"sort": "postal_code"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == CUSTOMER_3_NAME
    assert response_body[0]["id"] == CUSTOMER_3_ID
    assert response_body[0]["phone"] == CUSTOMER_3_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_3_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_1_NAME
    assert response_body[1]["id"] == CUSTOMER_1_ID
    assert response_body[1]["phone"] == CUSTOMER_1_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[2]["name"] == CUSTOMER_2_NAME
    assert response_body[2]["id"] == CUSTOMER_2_ID
    assert response_body[2]["phone"] == CUSTOMER_2_PHONE
    assert response_body[2]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_paginate_count_greater_than_num_customers(client, one_customer):
    # Arrange
    data = {"count": 5, "page_num": 1}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE


def test_get_second_page_of_customers(client, one_customer, second_customer):
    # Arrange
    data = {"count": 1, "page_num": 2}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_2_NAME
    assert response_body[0]["id"] == CUSTOMER_2_ID
    assert response_body[0]["phone"] == CUSTOMER_2_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_2_POSTAL_CODE

    
def test_get_first_page_of_customers_grouped_by_two(client, one_customer, second_customer, third_customer):
    # Arrange
    data = {"count": 2, "page_num": 1}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_second_page_of_customers_grouped_by_two(client, one_customer, second_customer, third_customer):
    # Arrange
    data = {"count": 2, "page_num": 2}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_3_NAME
    assert response_body[0]["id"] == CUSTOMER_3_ID
    assert response_body[0]["phone"] == CUSTOMER_3_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_3_POSTAL_CODE


def test_get_customers_no_page(client, one_customer, second_customer, third_customer):
    # Arrange
    data = {"count": 2}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_customers_sorted_and_paginated(client, one_customer, second_customer, third_customer):
    # Arrange
    data = {"count": 2, "sort": "name"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_3_NAME
    assert response_body[1]["id"] == CUSTOMER_3_ID
    assert response_body[1]["phone"] == CUSTOMER_3_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_3_POSTAL_CODE

def test_get_customers_invalid_sort_param(client, one_customer, second_customer):
    # Arrange
    data = {"sort": "invalid"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE


def test_get_customers_invalid_n_param(client, one_customer, second_customer):
    # Arrange
    data = {"count": "invalid"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_customers_invalid_p_param(client, one_customer, second_customer):
    # Arrange
    data = {"page_num": "invalid"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

# Test /customers/<id>/rentals


def test_get_rentals_no_query_params_sorts_by_id(client, one_checked_out_video, second_checked_out_video, third_checked_out_video):
    # Act
    response = client.get("/customers/1/rentals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[1]["id"] == VIDEO_2_ID
    assert response_body[1]["total_inventory"] == VIDEO_2_INVENTORY

    assert response_body[2]["title"] == VIDEO_3_TITLE
    assert response_body[2]["id"] == VIDEO_3_ID
    assert response_body[2]["total_inventory"] == VIDEO_3_INVENTORY
    
def test_get_rentals_sorted_by_title(client, one_checked_out_video, second_checked_out_video, third_checked_out_video):
    # Arrange
    data = {"sort": "title"}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_3_TITLE
    assert response_body[1]["id"] == VIDEO_3_ID
    assert response_body[1]["total_inventory"] == VIDEO_3_INVENTORY

    assert response_body[2]["title"] == VIDEO_2_TITLE
    assert response_body[2]["id"] == VIDEO_2_ID
    assert response_body[2]["total_inventory"] == VIDEO_2_INVENTORY

def test_get_paginate_n_greater_than_rentals(client, one_checked_out_video):
    # Arrange
    data = {"count": 5,"page_num": 1}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY


def test_get_second_page_of_rentals(client, one_checked_out_video, second_checked_out_video):
    # Arrange
    data = {"count": 1, "page_num": 2}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_2_TITLE
    assert response_body[0]["id"] == VIDEO_2_ID
    assert response_body[0]["total_inventory"] == VIDEO_2_INVENTORY

    
def test_get_first_page_of_rentals_grouped_by_two(client, one_checked_out_video, second_checked_out_video, third_checked_out_video):
    # Arrange
    data = {"count": 2, "page_num": 1}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[1]["id"] == VIDEO_2_ID
    assert response_body[1]["total_inventory"] == VIDEO_2_INVENTORY

def test_get_second_page_of_rentals_grouped_by_two(client, one_checked_out_video, second_checked_out_video, third_checked_out_video):
    # Arrange
    data = {"count": 2, "page_num": 2}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_3_TITLE
    assert response_body[0]["id"] == VIDEO_3_ID
    assert response_body[0]["total_inventory"] == VIDEO_3_INVENTORY

def test_get_rentals_no_page(client, one_checked_out_video, second_checked_out_video, third_checked_out_video):
    # Arrange
    data = {"count": 2}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[1]["id"] == VIDEO_2_ID
    assert response_body[1]["total_inventory"] == VIDEO_2_INVENTORY

def test_get_rentals_sorted_and_paginated(client, one_checked_out_video, second_checked_out_video, third_checked_out_video):
    # Arrange
    data = {"count": 2, "sort": "title", "page_num": 2}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_2_TITLE
    assert response_body[0]["id"] == VIDEO_2_ID
    assert response_body[0]["total_inventory"] == VIDEO_2_INVENTORY

def test_get_rentals_invalid_sort_param(client, one_checked_out_video, second_checked_out_video):
    # Arrange
    data = {"sort": "invalid"}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[1]["id"] == VIDEO_2_ID
    assert response_body[1]["total_inventory"] == VIDEO_2_INVENTORY

def test_get_rentals_invalid_n_param(client, one_checked_out_video, second_checked_out_video):
    # Arrange
    data = {"count": "invalid"}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[1]["id"] == VIDEO_2_ID
    assert response_body[1]["total_inventory"] == VIDEO_2_INVENTORY

def test_get_rentals_invalid_p_param(client, one_checked_out_video, second_checked_out_video):
    # Arrange
    data = {"page_num": "invalid"}

    # Act
    response = client.get("/customers/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[0]["id"] == VIDEO_1_ID
    assert response_body[0]["total_inventory"] == VIDEO_1_INVENTORY

    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[1]["id"] == VIDEO_2_ID
    assert response_body[1]["total_inventory"] == VIDEO_2_INVENTORY

# CUSTOMERS
def test_get_rentals_no_query_params_sorts_by_id(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Act
    response = client.get("/videos/1/rentals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

    assert response_body[2]["name"] == CUSTOMER_3_NAME
    assert response_body[2]["id"] == CUSTOMER_3_ID
    assert response_body[2]["phone"] == CUSTOMER_3_PHONE
    assert response_body[2]["postal_code"] == CUSTOMER_3_POSTAL_CODE

    
def test_get_renting_sorted_by_name(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Arrange
    data = {"sort": "name"}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_3_NAME
    assert response_body[1]["id"] == CUSTOMER_3_ID
    assert response_body[1]["phone"] == CUSTOMER_3_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_3_POSTAL_CODE

    assert response_body[2]["name"] == CUSTOMER_2_NAME
    assert response_body[2]["id"] == CUSTOMER_2_ID
    assert response_body[2]["phone"] == CUSTOMER_2_PHONE
    assert response_body[2]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_renters_sorted_by_postal_code(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Arrange
    data = {"sort": "postal_code"}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == CUSTOMER_3_NAME
    assert response_body[0]["id"] == CUSTOMER_3_ID
    assert response_body[0]["phone"] == CUSTOMER_3_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_3_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_1_NAME
    assert response_body[1]["id"] == CUSTOMER_1_ID
    assert response_body[1]["phone"] == CUSTOMER_1_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[2]["name"] == CUSTOMER_2_NAME
    assert response_body[2]["id"] == CUSTOMER_2_ID
    assert response_body[2]["phone"] == CUSTOMER_2_PHONE
    assert response_body[2]["postal_code"] == CUSTOMER_2_POSTAL_CODE


def test_paginate_count_greater_than_num_renters(client, customer_one_video_three):
    # Arrange
    data = {"count": 5, "page_num": 1}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE


def test_get_second_page_of_renters(client, customer_one_video_three, customer_two_video_three):
    # Arrange
    data = {"count": 1, "page_num": 2}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_2_NAME
    assert response_body[0]["id"] == CUSTOMER_2_ID
    assert response_body[0]["phone"] == CUSTOMER_2_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_2_POSTAL_CODE

    
def test_get_first_page_of_renters_grouped_by_two(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Arrange
    data = {"count": 2, "page_num": 1}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_second_page_of_renters_grouped_by_two(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Arrange
    data = {"count": 2, "page_num": 2}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_3_NAME
    assert response_body[0]["id"] == CUSTOMER_3_ID
    assert response_body[0]["phone"] == CUSTOMER_3_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_3_POSTAL_CODE


def test_get_renters_no_page(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Arrange
    data = {"count": 2}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_renters_sorted_and_paginated(client, customer_one_video_three, customer_two_video_three, customer_three_video_three):
    # Arrange
    data = {"count": 2, "sort": "name", "page_num": 1}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_3_NAME
    assert response_body[1]["id"] == CUSTOMER_3_ID
    assert response_body[1]["phone"] == CUSTOMER_3_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_3_POSTAL_CODE

def test_get_renters_invalid_sort_param(client, customer_one_video_three, customer_two_video_three):
    # Arrange
    data = {"sort": "invalid"}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE


def test_get_renters_invalid_n_param(client, customer_one_video_three, customer_two_video_three):
    # Arrange
    data = {"count": "invalid"}

    # Act
    response = client.get("/videos/1/rentals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE

def test_get_renters_invalid_p_param(client, customer_one_video_three, customer_two_video_three):
    # Arrange
    data = {"page_num": "invalid"}

    # Act
    response = client.get("/customers", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_1_NAME
    assert response_body[0]["id"] == CUSTOMER_1_ID
    assert response_body[0]["phone"] == CUSTOMER_1_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_1_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_2_NAME
    assert response_body[1]["id"] == CUSTOMER_2_ID
    assert response_body[1]["phone"] == CUSTOMER_2_PHONE
    assert response_body[1]["postal_code"] == CUSTOMER_2_POSTAL_CODE


