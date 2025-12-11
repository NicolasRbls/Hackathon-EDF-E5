from fastapi import status

def test_create_device(client, admin_token):
    response = client.post(
        "/devices/",
        json={"serial_number": "12345", "num_carton": "C1"},
        headers=admin_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["serial_number"] == "12345"

def test_create_device_duplicate(client, admin_token):
    # Create first time
    client.post("/devices/", json={"serial_number": "12345"}, headers=admin_token)
    # Create second time
    response = client.post("/devices/", json={"serial_number": "12345"}, headers=admin_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Device already registered"

def test_read_device(client, admin_token):
    # Setup
    client.post("/devices/", json={"serial_number": "TEST-READ"}, headers=admin_token)
    
    # Test
    response = client.get("/devices/TEST-READ")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "TEST-READ"

def test_read_device_not_found(client):
    response = client.get("/devices/UNKNOWN")
    assert response.status_code == 404
