from fastapi import status
import csv
import io

def test_search_devices(client, admin_token):
    # Setup
    client.post("/devices/", json={"serial_number": "SEARCH-1", "num_carton": "C-SEARCH", "operateur": "Orange"}, headers=admin_token)
    client.post("/devices/", json={"serial_number": "SEARCH-2", "num_carton": "C-SEARCH", "operateur": "Bouygues"}, headers=admin_token)
    client.post("/devices/", json={"serial_number": "S3", "num_carton": "C2", "operateur": "Orange"}, headers=admin_token)

    # Search by Carton
    res = client.get("/devices/search?num_carton=C-SEARCH")
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

def test_bulk_actions(client, admin_token):
    # Setup: 2 devices in Carton C-BULK
    client.post("/devices/", json={"serial_number": "BULK-1", "num_carton": "C-BULK"}, headers=admin_token)
    client.post("/devices/", json={"serial_number": "BULK-2", "num_carton": "C-BULK"}, headers=admin_token)
    
    # Perform Bulk Reception
    response = client.post("/actions/bulk", json={
        "action_type": "RECEPTION",
        "num_carton": "C-BULK",
        "user_id": "BulkUser"
    }, headers=admin_token)
    
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2
    
    # Verify Status Update
    d1 = client.get("/devices/BULK-1").json()
    d2 = client.get("/devices/BULK-2").json()
    assert d1["current_status"] == "en_stock"
    assert d2["current_status"] == "en_stock"

def test_dictionaries(client):
    response = client.get("/devices/dictionaries")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "affectation" in data
    assert "Magasin" in data["affectation"]

def test_export_csv(client, admin_token):
    client.post("/devices/", json={"serial_number": "EXPORT-1"}, headers=admin_token)
    
    res = client.get("/export/csv")
    assert res.status_code == 200
    assert "Serial Number" in res.text
    assert "EXPORT-1" in res.text
