def test_get_user(api_request_context):
    response = api_request_context.get("/users/1")
    assert response.status == 200
    data = response.json()
    assert data["id"]  == 1
    assert data["name"] == "Leanne Graham"
    assert data["email"] == "Sincere@april.biz"
    assert "address" in data
    assert "company" in data