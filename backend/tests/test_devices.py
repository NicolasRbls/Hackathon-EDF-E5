from fastapi import status

def test_create_device(client):
    response = client.post(
        "/devices/",
        json={"serial_number": "TEST-12345", "current_location": "Atelier"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["serial_number"] == "TEST-12345"
    assert data["current_status"] == "STOCK"  # Default value check
    assert "id" in data

def test_create_device_duplicate(client):
    # Create first time
    client.post("/devices/", json={"serial_number": "DUP-001"})
    # Create second time
    response = client.post("/devices/", json={"serial_number": "DUP-001"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_read_device(client):
    # Setup
    client.post("/devices/", json={"serial_number": "READ-ME"})
    
    # Test
    response = client.get("/devices/READ-ME")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["serial_number"] == "READ-ME"

def test_read_device_not_found(client):
    response = client.get("/devices/NON-EXISTENT")
    assert response.status_code == status.HTTP_404_NOT_FOUND
