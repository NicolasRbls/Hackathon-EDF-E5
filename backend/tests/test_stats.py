from fastapi import status
from app import models, security

def test_stats_stocks(client, admin_token):
    # 1. Setup Data
    
    # D1 Cluster: Carton C1 -> BO Nord -> Pose
    # Use headers=admin_token for device creation
    for i in range(4):
        client.post("/devices/", json={"serial_number": f"D1-{i}", "num_carton": "C1"}, headers=admin_token)
        
    client.post("/actions/bulk", json={"num_carton": "C1", "action_type": "RECEPTION", "user_id": "u"}, headers=admin_token)
    client.post("/actions/bulk", json={"num_carton": "C1", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "u"}, headers=admin_token)
    # Pose Single D1-0
    client.post("/actions/", json={"device_serial": "D1-0", "action_type": "POSE", "poste_pose": "P1", "user_id": "u"}, headers=admin_token)

    # D2 Cluster: Carton C2 -> Magasin Stock
    for i in range(4):
         client.post("/devices/", json={"serial_number": f"D2-{i}", "num_carton": "C2"}, headers=admin_token)
    client.post("/actions/bulk", json={"num_carton": "C2", "action_type": "RECEPTION", "user_id": "h"}, headers=admin_token)

    response = client.get("/stats/stocks", headers=admin_token)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Expect Structure: {"Magasin": {"en_stock": 4}, "BO Nord": {"pose": 1, "en_stock": 3}}
    assert "Magasin" in data
    assert data["Magasin"]["en_stock"] >= 4
    
    assert "BO Nord" in data
    assert data["BO Nord"]["pose"] >= 1

def test_dashboard_history(client, admin_token):
    # Setup Carton C3
    for i in range(4):
        client.post("/devices/", json={"serial_number": f"D3-{i}", "num_carton": "C3"}, headers=admin_token)

    client.post("/actions/bulk", json={"num_carton": "C3", "action_type": "RECEPTION", "user_id": "u"}, headers=admin_token)
    client.post("/actions/bulk", json={"num_carton": "C3", "action_type": "TRANSFERT", "new_affectation": "BO Sud", "user_id": "u"}, headers=admin_token)

    response = client.get("/dashboard/history", headers=admin_token)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # We expect at least 2 actions
    assert len(data) >= 2
    assert data[0]["action_type"] == "TRANSFERT" # Most recent first
