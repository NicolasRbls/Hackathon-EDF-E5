from app import security, models

def test_zone_permissions(client, db_session):
    # 1. Setup Users
    # Admin
    db_session.add(models.User(username="admin", password_hash=security.get_password_hash("pw"), role=models.UserRole.ADMIN))
    # BO Nord
    db_session.add(models.User(username="user_nord", password_hash=security.get_password_hash("pw"), role=models.UserRole.BO_NORD))
    # BO Sud
    db_session.add(models.User(username="user_sud", password_hash=security.get_password_hash("pw"), role=models.UserRole.BO_SUD))
    db_session.commit()
    
    # Get Tokens
    token_nord = client.post("/auth/login", data={"username": "user_nord", "password": "pw"}).json()["access_token"]
    header_nord = {"Authorization": f"Bearer {token_nord}"}
    
    token_sud = client.post("/auth/login", data={"username": "user_sud", "password": "pw"}).json()["access_token"]
    header_sud = {"Authorization": f"Bearer {token_sud}"}

    # 2. Setup Device in BO NORD
    # We need to manually place it there using Admin and Full Carton
    token_ul = client.post("/auth/login", data={"username": "admin", "password": "pw"}).json()["access_token"]
    header_admin = {"Authorization": f"Bearer {token_ul}"}
    
    # Create Carton of 4
    for i in range(4):
        client.post("/devices/", json={"serial_number": f"D-NORD-{i}", "num_carton": "C-NORD"}, headers=header_admin) 
    
    target_serial = "D-NORD-0"
    
    # Reception & Transfert via Bulk
    client.post("/actions/bulk", json={"num_carton": "C-NORD", "action_type": "RECEPTION", "user_id": "admin"}, headers=header_admin)
    client.post("/actions/bulk", json={"num_carton": "C-NORD", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "admin"}, headers=header_admin)
    
    # Now D-NORD-0 is in BO Nord.
    
    # 3. Test: BO Nord User tries to POSE (Should Pass)
    # Check if device exists first for debugging
    d_check = client.get(f"/devices/{target_serial}")
    assert d_check.status_code == 200, f"Device {target_serial} missing! {d_check.json()}"

    res = client.post("/actions/", json={
        "device_serial": target_serial, 
        "action_type": "POSE", 
        "poste_pose": "P1",
        "user_id": "ignored"
    }, headers=header_nord)
    assert res.status_code == 200
    
    # 4. Test: BO Sud User tries to DEPOSE (Should Fail - Wrong Zone)
    res_fail = client.post("/actions/", json={
        "device_serial": target_serial, 
        "action_type": "DEPOSE", 
        "user_id": "ignored"
    }, headers=header_sud)
    assert res_fail.status_code == 403
