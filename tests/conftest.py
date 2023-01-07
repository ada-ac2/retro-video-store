import pytest
from app import create_app
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import datetime
from flask.signals import request_finished

VIDEO_TITLE = "A Brand New Video"
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_video(app):
    new_video = Video(
        title=VIDEO_TITLE, 
        release_date=VIDEO_RELEASE_DATE,
        total_inventory=VIDEO_INVENTORY,
        )
    db.session.add(new_video)
    db.session.commit()

@pytest.fixture
def second_video(app):
    new_video = Video(
        title="Video Two", 
        release_date="12-31-2000",
        total_inventory=1,
        )
    db.session.add(new_video)
    db.session.commit()

@pytest.fixture
def third_video(app):
    new_video = Video(
        title="Video Three", 
        release_date="01-02-2001",
        total_inventory=1,
        )
    db.session.add(new_video)
    db.session.commit()

@pytest.fixture
def five_copies_video(app):
    new_video = Video(
        title=VIDEO_TITLE, 
        release_date=VIDEO_RELEASE_DATE,
        total_inventory=5,
        )
    db.session.add(new_video)
    db.session.commit()

@pytest.fixture
def one_customer(app):
    new_customer = Customer(
        name=CUSTOMER_NAME,
        postal_code=CUSTOMER_POSTAL_CODE,
        phone=CUSTOMER_PHONE
    )
    db.session.add(new_customer)
    db.session.commit()

@pytest.fixture
def second_customer(app):
    new_customer = Customer(
        name="Second Customer",
        postal_code="12345",
        phone="234-234-2345"
    )
    db.session.add(new_customer)
    db.session.commit()

@pytest.fixture
def third_customer(app):
    new_customer = Customer(
        name="Customer Three",
        postal_code= "12344",
        phone="000-000-0000"
    )
    db.session.add(new_customer)
    db.session.commit()

@pytest.fixture
def one_checked_out_video(app, client, one_customer, one_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

@pytest.fixture
def second_checked_out_video(app, client, one_customer, second_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 2
    })

@pytest.fixture
def third_checked_out_video(app, client, one_customer, third_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 3
    })

@pytest.fixture
def one_returned_video(app, client, one_customer, second_video):
    client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 2
    })

    response = client.post("/rentals/check-in", json = {
        "customer_id": 1,
        "video_id": 2
    })

@pytest.fixture
def customer_one_video_three(app, client, one_customer, five_copies_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

@pytest.fixture
def customer_two_video_three(app, client, second_customer, five_copies_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 2,
        "video_id": 1
    })

@pytest.fixture
def customer_three_video_three(app, client, third_customer, five_copies_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 3,
        "video_id": 1
    })


