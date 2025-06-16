def test_home_redirects(client):
    response = client.get("/")
    assert response.status_code == 302  # redirige a login
