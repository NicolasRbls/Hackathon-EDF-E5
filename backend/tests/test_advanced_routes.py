from fastapi import status
import csv
import io

def test_search_devices(client):
    # Setup
    client.post("/devices/", json={"serial_number": "S1", "num_carton": "C1", "operateur": "Orange"})
    client.post("/devices/", json={"serial_number": "S2", "num_carton": "C1", "operateur": "Bouygues"})
    client.post("/devices/", json={"serial_number": "S3", "num_carton": "C2", "operateur": "Orange"})

    # Search by Carton
    res = client.get("/devices/search?num_carton=C1")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    
    # Search by Operator
    res = client.get("/devices/search?operateur=Orange")
    assert len(res.json()) == 2
    
    # Fuzzy Search
    res = client.get("/devices/search?q=S3")
    assert len(res.json()) == 1
    assert res.json()[0]["serial_number"] == "S3"

from app import security, models

def test_bulk_actions(client, db_session):
    # 0. Setup Admin for Auth
    hashed = security.get_password_hash("admin123")
    admin = models.User(username="admin_bulk", password_hash=hashed, role=models.UserRole.ADMIN)
    db_session.add(admin)
    db_session.commit()
    
    login = client.post("/auth/login", data={"username": "admin_bulk", "password": "admin123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Setup: 2 devices in Carton C-BULK
    client.post("/devices/", json={"serial_number": "B1", "num_carton": "C-BULK"})
    client.post("/devices/", json={"serial_number": "B2", "num_carton": "C-BULK"})
    
    # Perform Bulk Reception
    response = client.post("/actions/bulk", json={
        "action_type": "RECEPTION",
        "num_carton": "C-BULK",
        "user_id": "BulkUser"
    }, headers=headers)
    
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2
    
    # Verify Status Update
    d1 = client.get("/devices/B1").json()
    d2 = client.get("/devices/B2").json()
    assert d1["current_status"] == "en_stock"
    assert d2["current_status"] == "en_stock"

def test_dictionaries(client):
    response = client.get("/devices/dictionaries")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "affectation" in data
    assert "Magasin" in data["affectation"]

def test_export_csv(client):
    client.post("/devices/", json={"serial_number": "EXPORT-1"})
    
    response = client.get("/export/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    
    content = response.text
    assert "Serial Number" in content
    assert "EXPORT-1" in content
