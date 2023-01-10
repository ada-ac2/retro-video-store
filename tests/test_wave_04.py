from app.models.video import Video
from tests.conftest import VIDEO_TITLE

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

def test_get_all_videos_no_query_params_sorted_by_id(client,one_video,second_video,third_video):
    response = client.get("/videos")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[2]["title"] == VIDEO_3_TITLE

def test_get_all_videos_query_param_sort_by_title(client,one_video,second_video,third_video):
    data = {"sort": "title"}
    response = client.get("videos", query_string = data)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[1]["title"] == VIDEO_3_TITLE
    assert response_body[2]["title"] == VIDEO_2_TITLE

def test_get_all_videos_query_param_sort_by_total_inventory(client, one_video, second_video, five_copies_video):
    data = {"sort": "total_inventory"}
    response = client.get("videos", query_string = data)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == VIDEO_1_TITLE
    assert response_body[1]["title"] == VIDEO_2_TITLE
    assert response_body[2]["title"] == VIDEO_TITLE

def test_get_all_videos_query_param_sort_by_release_date(client, one_video, second_video, third_video):
    data = {"sort": "release_date"}
    response = client.get("videos", query_string = data)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == VIDEO_2_TITLE
    assert response_body[1]["title"] == VIDEO_1_TITLE
    assert response_body[2]["title"] == VIDEO_3_TITLE


