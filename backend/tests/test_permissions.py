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
    # We need to manually place it there because 'user_nord' cant create devices or transfer from magasin (only magasin can).
    # So lets use Admin to setup the board.
    client.post("/devices/", json={"serial_number": "D-NORD", "affectation": "BO Nord", "current_status": "en_stock"}) 
    # Wait, POST /devices defaults to Magasin. We need a TRANSFERT.
    # Let's interact as Admin.
    token_ul = client.post("/auth/login", data={"username": "admin", "password": "pw"}).json()["access_token"]
    header_admin = {"Authorization": f"Bearer {token_ul}"}
    
    client.post("/devices/", json={"serial_number": "D-NORD"}, headers=header_admin) # Magasin/Livraison
    client.post("/actions/", json={"device_serial": "D-NORD", "action_type": "RECEPTION", "user_id": "admin"}, headers=header_admin)
    client.post("/actions/", json={"device_serial": "D-NORD", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "admin"}, headers=header_admin)
    
    # Now D-NORD is in BO Nord.
    
    # 3. Test: BO Nord User tries to POSE (Should Pass)
    res = client.post("/actions/", json={
        "device_serial": "D-NORD", 
        "action_type": "POSE", 
        "poste_pose": "P1",
        "user_id": "ignored"
    }, headers=header_nord)
    assert res.status_code == 200
    
    # 4. Test: BO Sud User tries to DEPOSE (Should Fail - Wrong Zone)
    res_fail = client.post("/actions/", json={
        "device_serial": "D-NORD", 
        "action_type": "DEPOSE", 
        "user_id": "ignored"
    }, headers=header_sud)
    assert res_fail.status_code == 403
