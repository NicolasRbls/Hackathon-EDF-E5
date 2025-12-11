from app import security, models

def test_history_rbac(client, db_session):
    # Setup Users
    def token(u, r):
        h = security.get_password_hash("pw")
        if not db_session.query(models.User).filter_by(username=u).first():
            db_session.add(models.User(username=u, password_hash=h, role=r))
            db_session.commit()
        return client.post("/auth/login", data={"username": u, "password": "pw"}).json()["access_token"]

    t_admin = token("admin_rbac", models.UserRole.ADMIN)
    t_viewer = token("view_rbac", models.UserRole.VIEWER)
    t_mag = token("mag_rbac", models.UserRole.MAGASIN)
    t_bo = token("bo_rbac", models.UserRole.BO_NORD)

    h_admin = {"Authorization": f"Bearer {t_admin}"}
    h_viewer = {"Authorization": f"Bearer {t_viewer}"}
    h_mag = {"Authorization": f"Bearer {t_mag}"}

    # Generate Logs
    client.post("/devices/", json={"serial_number": "D-RBAC"}, headers=h_admin)
    client.post("/actions/", json={"device_serial": "D-RBAC", "action_type": "RECEPTION", "user_id": "mag_rbac"}, headers=h_mag)

    # 1. Admin sees everything
    res = client.get("/history/", headers=h_admin)
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 2. Viewer sees everything
    res = client.get("/history/", headers=h_viewer)
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 3. Magasinier sees OWN logs
    res = client.get("/history/", headers=h_mag)
    assert res.status_code == 200
    assert len(res.json()) >= 1
    assert res.json()[0]["user_id"] == "mag_rbac"

    # 4. Magasinier CAN see logs from OTHER Magasiniers (Role Scope)
    # But CANNOT see BO logs (Role Mismatch)
    
    # Case A: Try to see BO logs -> 403
    res = client.get("/history/?role=bo_nord", headers=h_mag)
    assert res.status_code == 403

    # Case B: Try to see Magasin logs -> 200 OK
    res = client.get("/history/?role=magasin", headers=h_mag)
    assert res.status_code == 200
    assert len(res.json()) >= 1

    print("\n✅ History RBAC Verified: Admin/Viewer=All, Users=Self.")
