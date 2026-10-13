def test_post_car_returns_201_and_json(client):
    payload = {"make": "Ford", "model": "Fiesta", "year": 2018, "color": "Black"}
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"


# 自己写API测试：非法年份1800不被保存，返回422
def test_invalid_year_is_not_saved(client):
    bad_payload = {"make": "Tesla", "model": "Model3", "year": 1800, "color": "Grey"}
    resp_post = client.post("/api/cars", json=bad_payload)
    assert resp_post.status_code == 422

    resp_get = client.get("/api/cars")
    data = resp_get.json()
    assert data == []
