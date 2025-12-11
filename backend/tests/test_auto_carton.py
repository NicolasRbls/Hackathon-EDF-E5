from app import security, models

def test_auto_carton_move(client, db_session):
    # Auth
    hashed = security.get_password_hash("pw")
    db_session.add(models.User(username="admin_auto", password_hash=hashed, role=models.UserRole.ADMIN))
def test_auto_carton_move(client, admin_token):
    # 1. Create Carton with 4 devices
    serials = []
    for i in range(4):
        s = f"AC-{i}"
        serials.append(s)
        client.post("/devices/", json={"serial_number": s, "num_carton": "CARTON-AUTO"}, headers=admin_token)

    # 2. Reception Only Device 0 (Single Scan)
    # Expected: ALL 4 should become EN_STOCK
    res = client.post("/actions/", json={
        "device_serial": serials[0], # Only scan one
        "action_type": "RECEPTION",
        "user_id": "ign"
    }, headers=admin_token)
    assert res.status_code == 200
    
    # 3. Verify Peer (Device 3)
    d3 = client.get(f"/devices/{serials[3]}").json()
    assert d3["current_status"] == "en_stock"
    assert d3["affectation"] == "Magasin"
    
    # 4. Transfert Device 0 -> BO Centre
    # Expected: ALL 4 move to BO Centre
    res = client.post("/actions/", json={
        "device_serial": serials[0],
        "action_type": "TRANSFERT",
        "new_affectation": "BO Centre",
        "user_id": "ign"
    }, headers=admin_token)
    assert res.status_code == 200
    
    d3 = client.get(f"/devices/{serials[3]}").json()
    assert d3["affectation"] == "BO Centre"
