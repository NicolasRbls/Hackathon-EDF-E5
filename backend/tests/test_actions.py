from fastapi import status

def test_perform_action_lifecycle(client):
    # 1. Create Device (Starts EN_LIVRAISON / MAGASIN)
    client.post("/devices/", json={"serial_number": "ACT-001"})

    # 2. RECEPTION (Valid: en_livraison -> en_stock)
    res_reception = client.post("/actions/", json={
        "device_serial": "ACT-001",
        "action_type": "RECEPTION",
        "user_id": "Magasinier"
    })
    assert res_reception.status_code == status.HTTP_200_OK
    
    # 3. TRANSFERT TO BO (Valid: en_stock -> en_stock / BO Nord)
    res_transfert = client.post("/actions/", json={
        "device_serial": "ACT-001",
        "action_type": "TRANSFERT",
        "new_affectation": "BO Nord",
        "user_id": "Logistique"
    })
    assert res_transfert.status_code == status.HTTP_200_OK

    # 4. POSE (Valid: en_stock -> pose)
    res_pose = client.post("/actions/", json={
        "device_serial": "ACT-001",
        "action_type": "POSE",
        "poste_pose": "P-123",
        "user_id": "Tech1"
    })
    assert res_pose.status_code == status.HTTP_200_OK
    
    # Verify final state
    device = client.get("/devices/ACT-001").json()
    assert device["current_status"] == "pose"
    assert device["poste_pose"] == "P-123"

def test_perform_action_invalid_pose(client):
    # Create device (EN_LIVRAISON)
    client.post("/devices/", json={"serial_number": "FAIL-001"})
    
    # Try POSE immediately (Should fail, needs to be En Stock)
    response = client.post("/actions/", json={
        "device_serial": "FAIL-001",
        "action_type": "POSE",
        "poste_pose": "P-X",
        "user_id": "Tech1"
    })
    assert response.status_code == 400
    assert "must be in STOCK" in response.json()["detail"]

def test_perform_action_device_not_found(client):
    response = client.post("/actions/", json={
        "device_serial": "UNKNOWN",
        "action_type": "POSE",
        "user_id": "Ghost"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

