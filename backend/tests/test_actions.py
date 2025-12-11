from fastapi import status

def test_perform_action_lifecycle(client, admin_token):
    # 1. Create Device Cluster (Carton C1 Needs 4 devices)
    for i in range(4):
        s = f"ACT-00{i+1}"
        client.post("/devices/", json={"serial_number": s, "num_carton": "C1"}, headers=admin_token)
        
    target_device = "ACT-001"

    # 2. RECEPTION (Magasin) - MUST USE BULK CARTON
    response = client.post("/actions/bulk", json={
        "action_type": "RECEPTION",
        "num_carton": "C1",
        "user_id": "ignored" 
    }, headers=admin_token)
    assert response.status_code == 200
    
    # Verify State
    device = client.get(f"/devices/{target_device}").json()
    assert device["current_status"] == "en_stock"
    assert device["affectation"] == "Magasin"

    # 3. TRANSFERT (Magasin -> BO Nord) - MUST USE BULK CARTON
    response = client.post("/actions/bulk", json={
        "action_type": "TRANSFERT",
        "new_affectation": "BO Nord",
        "num_carton": "C1",
        "user_id": "ignored"
    }, headers=admin_token)
    assert response.status_code == 200
    
    device = client.get(f"/devices/{target_device}").json()
    assert device["affectation"] == "BO Nord"

    # 4. POSE (BO Nord)
    response = client.post("/actions/", json={
        "device_serial": "ACT-001",
        "action_type": "POSE",
        "poste_pose": "P-123",
        "user_id": "ignored"
    }, headers=admin_token)
    assert response.status_code == 200
    
    device = client.get("/devices/ACT-001").json()
    assert device["current_status"] == "pose"

def test_perform_action_invalid_pose(client, admin_token):
    # Device exists but is EN_LIVRAISON by default. POSE requires EN_STOCK.
    client.post("/devices/", json={"serial_number": "BAD-POSE"}, headers=admin_token)
    
    response = client.post("/actions/", json={
        "device_serial": "BAD-POSE",
        "action_type": "POSE",
        "poste_pose": "P1",
        "user_id": "u"
    }, headers=admin_token)
    
    assert response.status_code == 400
    assert "STOCK" in response.json()["detail"]

def test_perform_action_device_not_found(client, admin_token):
    response = client.post("/actions/", json={
        "device_serial": "UNKNOWN",
        "action_type": "RECEPTION",
        "user_id": "u"
    }, headers=admin_token)
    
    assert response.status_code == 404
