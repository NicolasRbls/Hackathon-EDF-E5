from app import security, models

def test_device_creation_rbac(client, db_session):
    # Setup Users
    def token(u, r):
        h = security.get_password_hash("pw")
        if not db_session.query(models.User).filter_by(username=u).first():
            db_session.add(models.User(username=u, password_hash=h, role=r))
            db_session.commit()
        return client.post("/auth/login", data={"username": u, "password": "pw"}).json()["access_token"]

    t_admin = token("admin_dev", models.UserRole.ADMIN)
    t_mag = token("mag_dev", models.UserRole.MAGASIN)
    t_labo = token("labo_dev", models.UserRole.LABO)
    t_bo = token("bo_dev", models.UserRole.BO_NORD)

    h_admin = {"Authorization": f"Bearer {t_admin}"}
    h_mag = {"Authorization": f"Bearer {t_mag}"}
    h_labo = {"Authorization": f"Bearer {t_labo}"}
    h_bo = {"Authorization": f"Bearer {t_bo}"}

    # 1. Admin CAN create
    r = client.post("/devices/", json={"serial_number": "DEV-ADMIN"}, headers=h_admin)
    assert r.status_code == 201

    # 2. Magasin CAN create
    r = client.post("/devices/", json={"serial_number": "DEV-MAG"}, headers=h_mag)
    assert r.status_code == 201

    # 3. Labo CAN create
    r = client.post("/devices/", json={"serial_number": "DEV-LABO"}, headers=h_labo)
    assert r.status_code == 201

    # 4. BO (Technician) CANNOT create -> 403
    r = client.post("/devices/", json={"serial_number": "DEV-BO"}, headers=h_bo)
    assert r.status_code == 403
    
    print("\n✅ Device Creation RBAC Verified.")
