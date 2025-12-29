def test_create_post(api_request_context):
    new_post = {
        "title": "Test Post",
        "body": "This is a test post body",
        "userId": 1
    }
    response = api_request_context.post("/posts", data=new_post)
    assert response.status == 201
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["body"] == "This is a test post body"
    assert data["userId"] == 1
    assert "id" in data