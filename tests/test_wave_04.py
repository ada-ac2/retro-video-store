from app.models.rental import Rental


def test_rental_over_due(client, customer_with_overdue):
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body[0]["video_id"] == 1
    assert response_body[0]["title"] == "A Brand New Video"
    assert response_body[0]["postal_code"] == "12345"

