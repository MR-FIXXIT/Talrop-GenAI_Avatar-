def test_create_tenant(client):
    payload = {"name": "Test Tenant"}
    response = client.post("/auth/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "tenant_id" in data
    assert "api_key" in data
