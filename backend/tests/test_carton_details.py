from app import models, security

def test_get_carton_details(client, admin_token, db_session):
    # 1. Setup Data: Create 3 devices in "CARTON-X"
    # We use admin_token because device creation is restricted.
    carton_id = "CARTON-X"
    
    devices = ["DEV-001", "DEV-002", "DEV-003"]
    for sn in devices:
        # Create device in specific carton
        res = client.post("/devices/", json={
            "serial_number": sn, 
            "num_carton": carton_id,
            "current_status": "en_stock" # Optional, defaults usually work
        }, headers=admin_token)
        assert res.status_code == 201

    # 2. Call the new route
    # Assuming the route will be /devices/carton/{num_carton}
    # Authenticated user should be able to see it. 
    # Let's use admin_token for reading too, or just a logged in user.
    # The requirement didn't specify strict RBAC for *reading* this, so we'll test with auth.
    
    response = client.get(f"/devices/carton/{carton_id}", headers=admin_token)
    
    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Should return a list of devices or a dict with devices?
    # User said "recup toute kes infos d'un carton avec ses devices".
    # A simple list of devices seems appropriate or an object {"num_carton": "...", "devices": [...]}.
    # Let's aim for a list of devices first as it's the most direct "devices inside".
    # Or maybe better: {"carton_id": "...", "count": 3, "devices": [...]}
    # I'll implement a clean response model.
    
    assert data["num_carton"] == carton_id
    assert len(data["devices"]) == 3
    assert data["devices"][0]["serial_number"] in devices
    
def test_get_carton_not_found(client, admin_token):
    res = client.get("/devices/carton/UNKNOWN-CARTON", headers=admin_token)
    # Be careful: An empty carton is just a list of 0 devices? 
    # Or 404 if "Carton" is not an entity but just a property?
    # Since Carton is not a DB table, just a column, asking for "UNKNOWN" just returns empty list usually.
    # But if we want to mimic "Carton Info", maybe 200 with empty list is fine.
    # Let's check logic: if no devices found, maybe just array empty.
    assert res.status_code == 200
    assert len(res.json()["devices"]) == 0
