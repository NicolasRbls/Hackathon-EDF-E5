from app import security, models

def test_geolocation_support(client, db_session):
    # Auth
    hashed = security.get_password_hash("pw")
    db_session.add(models.User(username="admin_geo", password_hash=hashed, role=models.UserRole.ADMIN))
    db_session.commit()
    t = client.post("/auth/login", data={"username": "admin_geo", "password": "pw"}).json()["access_token"]
    h = {"Authorization": f"Bearer {t}"}

    # Setup Device
    client.post("/devices/", json={"serial_number": "D-GEO"}, headers=h)
    
    # Process to Stock
    client.post("/actions/", json={"device_serial": "D-GEO", "action_type": "RECEPTION", "user_id": "u"}, headers=h)
    # Process to BO
    client.post("/actions/", json={"device_serial": "D-GEO", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "u"}, headers=h)
    
    # POSE with GPS
    lat, lon = 48.8566, 2.3522 # Paris
    res = client.post("/actions/", json={
        "device_serial": "D-GEO",
        "action_type": "POSE",
        "poste_pose": "P-GEO-1",
        "latitude": lat,
        "longitude": lon,
        "user_id": "u"
    }, headers=h)
    assert res.status_code == 200
    
    # Verify Data
    d = client.get("/devices/D-GEO").json()
    assert d["current_status"] == "pose"
    assert d["latitude"] == lat
    assert d["longitude"] == lon
    
    print("\n✅ Geolocation Saved Successfully")
