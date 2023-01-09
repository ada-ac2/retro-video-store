from app.models.rental import Rental


def test_rental_over_due(client, customer_with_overdue):
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body[0]["video_id"] == 1
    assert response_body[0]["title"] == "A Brand New Video"
    assert response_body[0]["postal_code"] == "12345"


def test_rental_over_due_no_record(client, one_checked_out_video):
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_customers_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/customers/1/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == "Video Two"


def test_get_customer_not_found_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/customers/2/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Customer 2 was not found"}


def test_get_invalid_customer_not_found_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/customers/g/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "g invalid"}


def test_get_customer_no_rental_history(client, one_checked_out_video):
    # Act
    response = client.get("/customers/1/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []


def test_get_customers_rental_history(client, one_checked_out_video, one_returned_video):
    # Act
    response = client.get("/customers/1/history")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == "Video Two"


def test_get_videos_not_found_rental_history(client, one_checked_out_video):
    # Act
    response = client.get("/videos/2/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Video 2 was not found"}


def test_get_invalid_video_not_found_rental_history(client, one_checked_out_video):
    # Act
    response = client.get("/videos/g/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "g invalid"}


def test_get_videos_no_rental_history(client, one_checked_out_video):
    # Act
    response = client.get("/videos/1/history")
    response_body = response.get_json()

    # Assert
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
    assert response_body[0]["customer_id"] == 1
