from app.models.video import Video
from app.models.customer import Customer

VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 1
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 1
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

def test_checkout_video(client, one_video, one_customer):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["video_id"] == 1
    assert response_body["customer_id"] == 1
    assert response_body["videos_checked_out_count"] == 1
    assert response_body["available_inventory"] == 0

def test_checkout_video_not_found(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 100
    })

    assert response.status_code == 404

def test_checkout_customer_video_not_found(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 100,
        "video_id": 1
    })

    assert response.status_code == 404

def test_checkout_video_no_video_id(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
    })

    assert response.status_code == 400

def test_checkout_video_no_customer_id(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "video_id": 1,
    })

    assert response.status_code == 400

def test_checkout_video_no_inventory(client, one_checked_out_video, second_customer):
    response = client.post("/rentals/check-out", json={
        "customer_id": 2,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Could not perform checkout"

def test_checkin_video(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["video_id"] == 1
    assert response_body["customer_id"] == 1
    assert response_body["videos_checked_out_count"] == 0
    assert response_body["available_inventory"] == 1

def test_checkin_video_no_customer_id(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "video_id": 1
    })

    assert response.status_code == 400

def test_checkin_video_no_video_id(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 1
    })

    assert response.status_code == 400

def test_checkin_video_not_found(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 100
    })

    assert response.status_code == 404

def test_checkin_customer_not_found(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 100,
        "video_id": 1
    })

    assert response.status_code == 404

def test_checkin_video_not_checked_out(client, one_video, one_customer):

    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "No outstanding rentals for customer 1 and video 1"}
    

def test_rentals_by_video(client, one_checked_out_video):
    response = client.get("/videos/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_NAME

def test_rentals_by_video_not_found(client):
    response = client.get("/videos/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == "Video 1 was not found"

def test_rentals_by_video_no_rentals(client, one_video):
    response = client.get("/videos/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_rentals_by_customer(client, one_checked_out_video):
    response = client.get("/customers/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_TITLE

def test_rentals_by_customer_not_found(client):
    response = client.get("/customers/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == "Customer 1 was not found"

def test_rentals_by_customer_no_rentals(client, one_customer):
    response = client.get("/customers/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_can_delete_customer_with_rental(client, one_checked_out_video):
    # Act
    response = client.delete("/customers/1")

    #Assert
    assert response.status_code == 200

def test_can_delete_video_with_rental(client, one_checked_out_video):
    # Act
    response = client.delete("/videos/1")

    #Assert
    assert response.status_code == 200

def test_cant_checkout_video_twice(client, one_checked_out_video):
    # Act
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    # Assert 
    assert response.status_code == 400


def test_cant_checkin_video_twice(client, one_checked_out_video):
    # Act
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    # Assert 
    assert response.status_code == 200

    # Act
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    # Assert 
    assert response.status_code == 400