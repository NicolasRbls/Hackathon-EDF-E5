from app import security, models

def test_dashboard_history_rbac(client, db_session):
    # Setup Users
    def token(u, r):
        h = security.get_password_hash("pw")
        if not db_session.query(models.User).filter_by(username=u).first():
            db_session.add(models.User(username=u, password_hash=h, role=r))
            db_session.commit()
        return client.post("/auth/login", data={"username": u, "password": "pw"}).json()["access_token"]

    t_admin = token("a_dash", models.UserRole.ADMIN)
    t_viewer = token("v_dash", models.UserRole.VIEWER)
    t_bo = token("b_dash", models.UserRole.BO_NORD)

    h_admin = {"Authorization": f"Bearer {t_admin}"}
    h_viewer = {"Authorization": f"Bearer {t_viewer}"}
    h_bo = {"Authorization": f"Bearer {t_bo}"}

    # 1. Admin CAN access
    res = client.get("/dashboard/history", headers=h_admin)
    assert res.status_code == 200

    # 2. Viewer CAN access
    res = client.get("/dashboard/history", headers=h_viewer)
    assert res.status_code == 200

    # 3. Technician (BO Nord) CANNOT access -> 403
    res = client.get("/dashboard/history", headers=h_bo)
    assert res.status_code == 403

    print("\n✅ Dashboard History RBAC Verified.")
