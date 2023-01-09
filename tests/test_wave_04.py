VIDEO_2_TITLE = "Video Two"
VIDEO_2_ID = 2
VIDEO_2_INVENTORY = 1
VIDEO_2_RELEASE_DATE = "12-31-2000"

CUSTOMER_1_NAME = "A Brand New Customer"
CUSTOMER_1_ID = 1
CUSTOMER_1_POSTAL_CODE = "12345"
CUSTOMER_1_PHONE = "123-123-1234"

#@pytest.mark.skip()
def test_get_customers_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/customers/1/history")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_2_TITLE

#@pytest.mark.skip()
def test_get_customer_not_found_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/customers/2/history")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 404
    assert response_body == {"message": "Customer 2 was not found"}

#@pytest.mark.skip()
def test_get_customer_no_rental_history(client, one_checked_out_video):
    # Act
    response = client.get("/customers/1/history")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []

def test_get_videos_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/videos/2/history")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_1_NAME