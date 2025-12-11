from app import security, models
from fastapi import status

def test_chaos_monkey(client, db_session):
    """
    Test edge cases, invalid transitions, and potential logic holes.
    """
    # Auth Setup
    hashed = security.get_password_hash("pw")
    db_session.add(models.User(username="admin_chaos", password_hash=hashed, role=models.UserRole.ADMIN))
    db_session.commit()
    token = client.post("/auth/login", data={"username": "admin_chaos", "password": "pw"}).json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}

    # 1. INVALID TRANSITION: Depose an item that is EN_LIVRAISON
    # Setup
    client.post("/devices/", json={"serial_number": "D-CHAOS-1"}, headers=h)
    
    # Attempt DEPOSE (Should be POSE -> DEPOSE only)
    res = client.post("/actions/", json={
        "device_serial": "D-CHAOS-1",
        "action_type": "DEPOSE",
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 400
    assert "must be installed (POSE)" in res.json()["detail"]

    # 2. INVALID DATA: Unknown Enum
    res = client.post("/actions/", json={
        "device_serial": "D-CHAOS-1",
        "action_type": "DANCE_PARTY", # Invalid Enum
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 422 # Struct validation error

    # 3. CARTON INTEGRITY: Broken Carton Logistics
    # Create an incomplete carton (3 items)
    for i in range(3):
        client.post("/devices/", json={"serial_number": f"D-BROKEN-{i}", "num_carton": "C-BROKEN"}, headers=h)
        
    # Attempt Reception via Auto-Scan of 1 device
    res = client.post("/actions/", json={
        "device_serial": "D-BROKEN-0",
        "action_type": "RECEPTION",
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 400
    assert "incomplete" in res.json()["detail"]

    # 4. DOUBLE SCAN: Receive item twice
    # Fix the carton first to make it valid
    client.post("/devices/", json={"serial_number": "D-BROKEN-3", "num_carton": "C-BROKEN"}, headers=h)
    
    # First Rec
    res = client.post("/actions/", json={
        "device_serial": "D-BROKEN-0",
        "action_type": "RECEPTION",
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 200
    
    # Second Rec (Should be idempotent or authorized? Logic says pass but check warnings?)
    # Current logic: "if current_status != EN_LIVRAISON: pass"
    res = client.post("/actions/", json={
        "device_serial": "D-BROKEN-0",
        "action_type": "RECEPTION",
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 200 # Allowed to re-scan for now (idempotence)

    # 5. POSE WITHOUT POSTE
    # Move to BO
    client.post("/actions/", json={"device_serial": "D-BROKEN-0", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "u"}, headers=h)
    
    # Try Pose without 'poste_pose'
    res = client.post("/actions/", json={
        "device_serial": "D-BROKEN-0",
        "action_type": "POSE",
        # Missing poste_pose
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 400
    assert "Poste Pose required" in res.json()["detail"]

    print("\n✅ Chaos Monkey Survived: All edge cases handled gracefully.")
