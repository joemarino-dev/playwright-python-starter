def test_get_single_post(api_request_context):
    response = api_request_context.get("/posts/1")
    assert response.status == 200
    data = response.json()
    assert data["userId"] == 1
    assert data["id"] == 1
    assert "title" in data
    assert "body" in data
    assert len(data["title"]) > 0