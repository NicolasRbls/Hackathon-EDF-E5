from fastapi import status

def test_stats_stocks(client):
    # Setup Data
    # D1: Create -> Reception -> Transfert BO -> Pose (Status: POSE, Aff: BO Nord)
    client.post("/devices/", json={"serial_number": "D1"})
    client.post("/actions/", json={"device_serial": "D1", "action_type": "RECEPTION", "user_id": "u"})
    client.post("/actions/", json={"device_serial": "D1", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "u"})
    client.post("/actions/", json={"device_serial": "D1", "action_type": "POSE", "poste_pose": "P1", "user_id": "u"})

    # D2: Create -> Reception (Status: EN_STOCK, Aff: Magasin)
    client.post("/devices/", json={"serial_number": "D2"})
    client.post("/actions/", json={"device_serial": "D2", "action_type": "RECEPTION", "user_id": "u"})

    response = client.get("/stats/stocks")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Expect Structure: {"Magasin": {"en_stock": 1}, "BO Nord": {"pose": 1}}
    assert "Magasin" in data
    assert data["Magasin"]["en_stock"] == 1
    
    assert "BO Nord" in data
    assert data["BO Nord"]["pose"] == 1

def test_dashboard_history(client):
    client.post("/devices/", json={"serial_number": "D3"})
    client.post("/actions/", json={"device_serial": "D3", "action_type": "RECEPTION", "user_id": "u"})
    client.post("/actions/", json={"device_serial": "D3", "action_type": "TRANSFERT", "new_affectation": "BO Sud", "user_id": "u"})

    response = client.get("/dashboard/history")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # We expect at least 2 actions
    assert len(data) >= 2
    assert data[0]["action_type"] == "TRANSFERT" # Most recent first
    # Ensure DESC order (transfert most recent)
    assert data[0]["action_type"] == "TRANSFERT"
