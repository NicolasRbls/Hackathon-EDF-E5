from fastapi import status
from app import models

def test_perform_action_pose(client):
    # 1. Create Device
    client.post("/devices/", json={"serial_number": "ACT-001"})
    
    # 2. Perform POSE
    response = client.post("/actions/", json={
        "serial_number": "ACT-001",
        "action_type": "POSE",
        "location": "Poste P12",
        "user_id": "Tech1"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["action_type"] == "POSE"
    assert data["location"] == "Poste P12"
    
    # 3. Verify Device Status Updated
    dev_response = client.get("/devices/ACT-001")
    dev_data = dev_response.json()
    assert dev_data["current_status"] == "EN_SERVICE"
    assert dev_data["current_location"] == "Poste P12"

def test_perform_action_device_not_found(client):
    response = client.post("/actions/", json={
        "serial_number": "UNKNOWN",
        "action_type": "POSE"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
