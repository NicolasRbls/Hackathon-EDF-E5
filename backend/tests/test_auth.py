from app import models, security
from app.database import get_db

def test_auth_full_cycle(client, db_session):
    # 1. Seeding: Create an Admin directly in DB
    hashed = security.get_password_hash("admin123")
    admin = models.User(username="admin_test", password_hash=hashed, role=models.UserRole.ADMIN)
    db_session.add(admin)
    db_session.commit()
    
    # 2. Login as Admin
    login_res = client.post("/auth/login", data={"username": "admin_test", "password": "admin123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create a Magasin User
    res_create = client.post("/auth/users", json={
        "username": "magasinier_1",
        "password": "magpass",
        "role": "magasin"
    }, headers=headers)
    assert res_create.status_code == 200
    assert res_create.json()["username"] == "magasinier_1"
    
    # 4. Login as Magasin User
    login_mag = client.post("/auth/login", data={"username": "magasinier_1", "password": "magpass"})
    token_mag = login_mag.json()["access_token"]
    headers_mag = {"Authorization": f"Bearer {token_mag}"}
    
    # 5. Verify Magasin cannot create other users
    res_fail = client.post("/auth/users", json={
        "username": "hacker",
        "password": "pw",
        "role": "admin"
    }, headers=headers_mag)
    assert res_fail.status_code == 403

def test_logout(client):
    res = client.post("/auth/logout")
    assert res.status_code == 200
    assert res.json() == {"message": "Successfully logged out"}
