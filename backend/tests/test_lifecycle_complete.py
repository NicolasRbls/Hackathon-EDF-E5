from app import security, models

def test_full_device_lifecycle(client, db_session):
    """
    Simulates the complete journey of a device group (Carton) through the EDF ecosystem.
    Actors: Admin, Magasinier, Tech Nord, Tech Sud (Attacker), Labo.
    """
    
    # --- 1. SETUP ACTORS ---
    def create_actor(username, role):
        hashed = security.get_password_hash("pw")
        db_session.add(models.User(username=username, password_hash=hashed, role=role))
        db_session.commit()
        token = client.post("/auth/login", data={"username": username, "password": "pw"}).json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    auth_admin = create_actor("admin_life", models.UserRole.ADMIN)
    auth_magasin = create_actor("mag_life", models.UserRole.MAGASIN)
    auth_nord = create_actor("tech_nord", models.UserRole.BO_NORD)
    auth_sud = create_actor("tech_sud", models.UserRole.BO_SUD) # The intruder
    auth_labo = create_actor("labo_life", models.UserRole.LABO)

    # --- 2. IMPORT / CREATION (Admin work, usually) ---
    # Create Carton "C-LIFE" with 4 devices
    carton_id = "C-LIFE"
    serials = [f"LIFE-{i}" for i in range(4)]
    
    for s in serials:
        # Created in "EN_LIVRAISON" at "MAGASIN"
        res = client.post("/devices/", json={"serial_number": s, "num_carton": carton_id}, headers=auth_admin)
        assert res.status_code == 201

    target_serial = serials[0]

    # --- 3. RECEPTION (Magasinier) ---
    # Using Single Scan Auto-Carton feature
    res = client.post("/actions/", json={
        "device_serial": target_serial,
        "action_type": "RECEPTION",
        "user_id": "mag_life" 
    }, headers=auth_magasin)
    assert res.status_code == 200, f"Magasinier failed to RECEPTION: {res.json()}"
    
    # Verify Status: EN_STOCK, MAGASIN
    d = client.get(f"/devices/{target_serial}").json()
    assert d["current_status"] == "en_stock"
    assert d["affectation"] == "Magasin"

    # --- 4. TRANSFERT (Magasinier -> BO Nord) ---
    res = client.post("/actions/", json={
        "device_serial": target_serial,
        "action_type": "TRANSFERT",
        "new_affectation": "BO Nord",
        "user_id": "mag_life"
    }, headers=auth_magasin)
    assert res.status_code == 200

    d = client.get(f"/devices/{serials[3]}").json() # Check implicit peer
    assert d["affectation"] == "BO Nord"

    # --- 5. ATTEMPTED THEFT (Tech Sud tries to install it) ---
    res = client.post("/actions/", json={
        "device_serial": target_serial,
        "action_type": "POSE",
        "poste_pose": "P-SUD",
        "user_id": "tech_sud"
    }, headers=auth_sud)
    assert res.status_code == 403, "Security Alert: BO Sud accessed BO Nord device!"

    # --- 6. INSTALLATION / POSE (Tech Nord) ---
    res = client.post("/actions/", json={
        "device_serial": target_serial,
        "action_type": "POSE",
        "poste_pose": "P-NORD-1",
        "user_id": "tech_nord"
    }, headers=auth_nord)
    assert res.status_code == 200
    
    d = client.get(f"/devices/{target_serial}").json()
    assert d["current_status"] == "pose"
    assert d["poste_pose"] == "P-NORD-1"
    
    # Verify peer is still EN_STOCK (Carton was split for installation)
    d_peer = client.get(f"/devices/{serials[1]}").json()
    assert d_peer["current_status"] == "en_stock"

    # --- 7. DEPOSE (Tech Nord) ---
    # Removal for maintenance
    res = client.post("/actions/", json={
        "device_serial": target_serial,
        "action_type": "DEPOSE",
        "user_id": "tech_nord"
    }, headers=auth_nord)
    assert res.status_code == 200
    
    d = client.get(f"/devices/{target_serial}").json()
    assert d["current_status"] == "a_tester"
    assert d["affectation"] == "Labo" # Auto-sent to Labo

    # --- 8. LABO EXPERTISE (Labo User) ---
    res = client.post("/actions/", json={
        "device_serial": target_serial,
        "action_type": "TEST",
        "new_status": "en_stock", # Validated OK
        "user_id": "labo_life"
    }, headers=auth_labo)
    assert res.status_code == 200

    d = client.get(f"/devices/{target_serial}").json()
    assert d["current_status"] == "en_stock"
    assert d["affectation"] == "Magasin" # Returned to stock

    print("\n✅ Full Lifecycle Validated: Import -> Rec -> Trans -> Pose -> Depose -> Labo -> Stock")
