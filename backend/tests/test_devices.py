from fastapi import status

def test_create_device(client):
    response = client.post(
        "/devices/",
        json={"serial_number": "TEST-12345", "num_carton": "C100"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["serial_number"] == "TEST-12345"
    assert data["current_status"] == "en_livraison"  # Default
    assert data["affectation"] == "Magasin" # Default
    assert data["num_carton"] == "C100"

def test_create_device_duplicate(client):
    # Create first time
    client.post("/devices/", json={"serial_number": "TEST-DUP"})
    # Create second time
    response = client.post("/devices/", json={"serial_number": "TEST-DUP"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Device already registered"

def test_read_device(client):
    # Setup
    client.post("/devices/", json={"serial_number": "TEST-READ"})
    
    # Test
    response = client.get("/devices/TEST-READ")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "TEST-READ"

def test_read_device_not_found(client):
    response = client.get("/devices/UNKNOWN")
    assert response.status_code == 404
