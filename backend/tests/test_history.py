from app import security, models

def test_history_search(client, db_session):
    # Setup: Create 2 users (Magasinier, BO Nord)
    def create_user(u, r, p="pw"):
        h = security.get_password_hash(p)
        db_session.add(models.User(username=u, password_hash=h, role=r))
        db_session.commit()
        return client.post("/auth/login", data={"username": u, "password": p}).json()["access_token"]

    t_mag = create_user("mag_hist", models.UserRole.MAGASIN)
    t_bo = create_user("bo_hist", models.UserRole.BO_NORD)
    
    h_admin = {"Authorization": f"Bearer {create_user('admin_hist', models.UserRole.ADMIN)}"}
    h_mag = {"Authorization": f"Bearer {t_mag}"}
    h_bo = {"Authorization": f"Bearer {t_bo}"}

    # Create Devices and Perform Actions to generate History
    # Magasinier receives D1
    client.post("/devices/", json={"serial_number": "D-HIST-1"}, headers=h_admin)
    client.post("/actions/", json={"device_serial": "D-HIST-1", "action_type": "RECEPTION", "user_id": "mag_hist"}, headers=h_mag)
    
    # BO Nord poses D2 (Assume transfer done or just force created there)
    # Let's just create D2 and assume BO Nord acts on it (simulating)
    # Actually BO Nord needs permissions. D2 needs to be in BO Nord.
    client.post("/devices/", json={"serial_number": "D-HIST-2"}, headers=h_admin)
    client.post("/actions/", json={"device_serial": "D-HIST-2", "action_type": "RECEPTION", "user_id": "mag_hist"}, headers=h_mag)
    client.post("/actions/", json={"device_serial": "D-HIST-2", "action_type": "TRANSFERT", "new_affectation": "BO Nord", "user_id": "mag_hist"}, headers=h_mag)
    client.post("/actions/", json={"device_serial": "D-HIST-2", "action_type": "POSE", "poste_pose": "P-HIST", "user_id": "bo_hist"}, headers=h_bo)

    # Now Search!
    
    # 1. Search by Role: MAGASIN
    # Should see RECEPTION of D1, RECEPTION of D2, TRANSFERT of D2
    res = client.get("/history/?role=magasin", headers=h_admin)
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) >= 3
    for log in logs:
        assert log["user_id"] == "mag_hist"

    # 2. Search by Role: BO_NORD
    # Should see POSE of D2
    res = client.get("/history/?role=bo_nord", headers=h_admin)
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) >= 1
    assert logs[0]["action_type"] == "POSE"
    assert logs[0]["user_id"] == "bo_hist"

    # 3. Search by Action: TRANSFERT
    res = client.get("/history/?action_type=TRANSFERT", headers=h_admin)
    assert len(res.json()) >= 1
    assert res.json()[0]["action_type"] == "TRANSFERT"

    print("\n✅ History Search Verified: Filters work correctly.")
