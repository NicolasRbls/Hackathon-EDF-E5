from app import models, security

def test_carton_capacity(client, db_session):
    # Auth
    hashed = security.get_password_hash("pw")
    db_session.add(models.User(username="admin_carton", password_hash=hashed, role=models.UserRole.ADMIN))
    db_session.commit()
    t = client.post("/auth/login", data={"username": "admin_carton", "password": "pw"}).json()["access_token"]
    h = {"Authorization": f"Bearer {t}"}

    # 1. Fill Carton C-FULL with 4 devices
    for i in range(4):
        res = client.post("/devices/", json={"serial_number": f"D-Fill-{i}", "num_carton": "C-FULL"})
        assert res.status_code == 201

    # 2. Try adding 5th device
    res_fail = client.post("/devices/", json={"serial_number": "D-Overflow", "num_carton": "C-FULL"})
    
    # 3. Expect Failure
    assert res_fail.status_code == 400
    assert "Carton C-FULL is full" in res_fail.json()["detail"]
