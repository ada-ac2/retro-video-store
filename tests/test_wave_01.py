from operator import contains
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

# --------------------------------
# ----------- VIDEOS -------------
# --------------------------------

# READ
def test_get_videos_no_saved_videos(client):
    # Act
    response = client.get("/videos")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_videos_one_saved_video(client, one_video):
    # Act
    response = client.get("/videos")
    response_body = response.get_json()
    print(response_body)

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["id"] == VIDEO_ID
    assert response_body[0]["total_inventory"] == VIDEO_INVENTORY

def test_get_video(client, one_video):
    # Act
    response = client.get("/videos/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["title"] == VIDEO_TITLE
    assert response_body["id"] == VIDEO_ID
    assert response_body["total_inventory"] == VIDEO_INVENTORY

def test_get_video_not_found(client):
    # Act
    response = client.get("/videos/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Video 1 was not found"}

def test_get_invalid_video_id(client, one_video):
    # Act
    response = client.get("/videos/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400


# CREATE
def test_create_video(client):
    # Act
    response = client.post("/videos", json={
        "title": VIDEO_TITLE,
        "release_date": VIDEO_RELEASE_DATE,
        "total_inventory": VIDEO_INVENTORY
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == VIDEO_TITLE
    assert response_body["id"] == VIDEO_ID
    assert response_body["total_inventory"] == VIDEO_INVENTORY

    new_video = Video.query.get(1)

    assert new_video
    assert new_video.title == VIDEO_TITLE

def test_create_video_must_contain_title(client):
    # Act
    response = client.post("/videos", json={
        "release_date": VIDEO_RELEASE_DATE,
        "total_inventory": VIDEO_INVENTORY
    })
    response_body = response.get_json()

    # Assert
    assert "details" in response_body
    assert "Request body must include title." in response_body["details"]
    assert response.status_code == 400
    assert Video.query.all() == []

def test_create_video_must_contain_release_date(client):
    # Act
    response = client.post("/videos", json={
        "title": VIDEO_TITLE,
        "total_inventory": VIDEO_INVENTORY
    })
    response_body = response.get_json()

    # Assert
    assert "details" in response_body
    assert "Request body must include release_date." in response_body["details"]
    assert response.status_code == 400
    assert Video.query.all() == []

def test_create_video_must_contain_inventory(client):
    # Act
    response = client.post("/videos", json={
        "title": VIDEO_TITLE,
        "release_date": VIDEO_RELEASE_DATE
    })
    response_body = response.get_json()

    assert "details" in response_body
    assert "Request body must include total_inventory." in response_body["details"]
    assert response.status_code == 400
    assert Video.query.all() == []

# DELETE
def test_delete_video(client, one_video):
    # Act
    response = client.delete("/videos/1")
    response_body = response.get_json()
    print("********", response)

    # Assert
    assert response_body["id"] == 1
    assert response.status_code == 200
    assert Video.query.get(1) == None

def test_delete_video_not_found(client):
    # Act
    response = client.delete("/videos/1")
    response_body = response.get_json()

    # Assert
    assert response_body == {"message": "Video 1 was not found"}
    assert response.status_code == 404
    assert Video.query.all() == []

def test_update_video(client, one_video):
    # Act
    response = client.put("/videos/1", json={
        "title": "Updated Video Title",
        "total_inventory": 2,
        "release_date": "01-01-2021"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["title"] == "Updated Video Title"
    assert response_body["total_inventory"] == 2

    video = Video.query.get(1)

    assert video.title == "Updated Video Title"
    assert video.total_inventory == 2

def test_update_video_not_found(client):
    # Act
    response = client.put("/videos/1", json={
        "title": "Updated Video Title",
        "total_inventory": 2,
        "release_date": "01-01-2021"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Video 1 was not found"}

def test_update_video_invalid_data(client, one_video):
    # Act
    response = client.put("/videos/1", json={
        "total_inventory": 2,
        "release_date": "01-01-2021"
    })

    # Assert
    assert response.status_code == 400 


# --------------------------------
# ----------- CUSTOMERS ----------
# --------------------------------

# READ
def test_get_customers_no_saved_customers(client):
    # Act
    response = client.get("/customers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_customers_one_saved_customer(client, one_customer):
    # Act
    response = client.get("/customers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == CUSTOMER_NAME
    assert response_body[0]["id"] == CUSTOMER_ID
    assert response_body[0]["phone"] == CUSTOMER_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_POSTAL_CODE

def test_get_customer(client, one_customer):
    # Act
    response = client.get("/customers/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["name"] == CUSTOMER_NAME
    assert response_body["id"] == CUSTOMER_ID
    assert response_body["phone"] == CUSTOMER_PHONE
    assert response_body["postal_code"] == CUSTOMER_POSTAL_CODE

def test_get_customer_not_found(client):
    # Act
    response = client.get("/customers/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Customer 1 was not found"}

def test_get_invalid_customer_id(client, one_customer):
    # Act
    response = client.get("/customers/hello")

    # Assert
    assert response.status_code == 400

# CREATE
def test_create_customer(client):
    # Act
    response = client.post("/customers", json={
        "name": CUSTOMER_NAME,
        "phone": CUSTOMER_PHONE,
        "postal_code": CUSTOMER_POSTAL_CODE
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == CUSTOMER_ID

    new_customer = Customer.query.get(1)

    assert new_customer
    assert new_customer.name == CUSTOMER_NAME
    assert new_customer.postal_code == CUSTOMER_POSTAL_CODE
    assert new_customer.phone == CUSTOMER_PHONE

def test_create_customer_must_contain_postal(client):
    # Act
    response = client.post("/customers", json={
        "name": CUSTOMER_NAME,
        "phone": CUSTOMER_PHONE,
    })
    response_body = response.get_json()

    # Assert
    assert "details" in response_body
    assert "Request body must include postal_code." in response_body["details"]
    assert response.status_code == 400
    assert Customer.query.all() == []

def test_create_customer_must_contain_name(client):
    # Act
    response = client.post("/customers", json={
        "phone": CUSTOMER_PHONE,
        "postal_code": CUSTOMER_POSTAL_CODE
    })
    response_body = response.get_json()

    # Assert
    assert "details" in response_body
    assert "Request body must include name." in response_body["details"]
    assert response.status_code == 400
    assert Customer.query.all() == []

def test_create_customer_must_contain_phone(client):
    # Act
    response = client.post("/customers", json={
        "name": CUSTOMER_NAME,
        "postal_code": CUSTOMER_POSTAL_CODE
    })
    response_body = response.get_json()

    assert "details" in response_body
    assert "Request body must include phone." in response_body["details"]
    assert response.status_code == 400
    assert Customer.query.all() == []

# DELETE
def test_delete_customer(client, one_customer):
    # Act
    response = client.delete("/customers/1")
    response_body = response.get_json()

    # Assert
    assert response_body["id"] == 1
    assert response.status_code == 200
    assert Customer.query.get(1) == None

def test_delete_customer_not_found(client):
    # Act
    response = client.delete("/customers/1")
    response_body = response.get_json()

    # Assert
    assert response_body == {"message": "Customer 1 was not found"}
    assert response.status_code == 404
    assert Customer.query.all() == []

def test_update_customer(client, one_customer):
    # Act
    response = client.put("/customers/1", json={
        "name": f"Updated ${CUSTOMER_NAME}",
        "phone": f"Updated ${CUSTOMER_PHONE}",
        "postal_code": f"Updated ${CUSTOMER_POSTAL_CODE}"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["name"] == f"Updated ${CUSTOMER_NAME}"
    assert response_body["phone"] == f"Updated ${CUSTOMER_PHONE}"
    assert response_body["postal_code"] == f"Updated ${CUSTOMER_POSTAL_CODE}"

    customer = Customer.query.get(1)
    assert customer.name == f"Updated ${CUSTOMER_NAME}"
    assert customer.phone == f"Updated ${CUSTOMER_PHONE}"
    assert customer.postal_code == f"Updated ${CUSTOMER_POSTAL_CODE}"
    

def test_update_customer_not_found(client):
    # Act
    response = client.put("/customers/1", json={
        "name": f"Updated ${CUSTOMER_NAME}",
        "phone": f"Updated ${CUSTOMER_PHONE}",
        "postal_code": f"Updated ${CUSTOMER_POSTAL_CODE}"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Customer 1 was not found"}

def test_update_customer_invalid_data(client, one_customer):
    # Act
    response = client.put("/customers/1", json={
        "phone": f"Updated ${CUSTOMER_PHONE}",
        "postal_code": f"Updated ${CUSTOMER_POSTAL_CODE}"
    })

    # Assert
    assert response.status_code == 400






