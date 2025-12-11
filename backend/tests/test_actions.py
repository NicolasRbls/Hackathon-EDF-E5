from fastapi import status

from app import models, security

def test_perform_action_lifecycle(client, db_session):
    # 0. Auth Setup
    hashed = security.get_password_hash("admin123")
    admin = models.User(username="admin_test", password_hash=hashed, role=models.UserRole.ADMIN)
    db_session.add(admin)
    db_session.commit()
    
    token = client.post("/auth/login", data={"username": "admin_test", "password": "admin123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Device Cluster (Carton C1 Needs 4 devices)
    for i in range(4):
        s = f"ACT-00{i+1}"
        client.post("/devices/", json={"serial_number": s, "num_carton": "C1"})
        
    target_device = "ACT-001"

    # 2. RECEPTION (Magasin) - MUST USE BULK CARTON
    response = client.post("/actions/bulk", json={
        "action_type": "RECEPTION",
        "num_carton": "C1",
        "user_id": "ignored" 
    }, headers=headers)
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
    }, headers=headers)
    assert response.status_code == 200
    
    device = client.get(f"/devices/{target_device}").json()
    assert device["affectation"] == "BO Nord"

    # 4. POSE (BO Nord)
    response = client.post("/actions/", json={
        "device_serial": "ACT-001",
        "action_type": "POSE",
        "poste_pose": "P-123", # Required
        "user_id": "ignored"
    }, headers=headers)
    assert response.status_code == 200
    
    device = client.get("/devices/ACT-001").json()
    assert device["current_status"] == "pose"

def test_perform_action_invalid_pose(client, db_session):
    # Auth
    hashed = security.get_password_hash("pw")
    db_session.add(models.User(username="a", password_hash=hashed, role=models.UserRole.ADMIN))
    db_session.commit()
    t = client.post("/auth/login", data={"username": "a", "password": "pw"}).json()["access_token"]
    h = {"Authorization": f"Bearer {t}"}

    client.post("/devices/", json={"serial_number": "BAD-POSE"})
    # Device is EN_LIVRAISON by default. POSE requires EN_STOCK.
    
    response = client.post("/actions/", json={
        "device_serial": "BAD-POSE",
        "action_type": "POSE",
        "poste_pose": "P1",
        "user_id": "u"
    }, headers=h)
    
    assert response.status_code == 400
    assert "STOCK" in response.json()["detail"]

def test_perform_action_device_not_found(client, db_session):
    # Auth
    hashed = security.get_password_hash("pw")
    db_session.add(models.User(username="a", password_hash=hashed, role=models.UserRole.ADMIN))
    db_session.commit()
    t = client.post("/auth/login", data={"username": "a", "password": "pw"}).json()["access_token"]
    h = {"Authorization": f"Bearer {t}"}

    response = client.post("/actions/", json={
        "device_serial": "UNKNOWN",
        "action_type": "RECEPTION",
        "user_id": "u"
    }, headers=h)
    
    assert response.status_code == 404
status.HTTP_404_NOT_FOUND
