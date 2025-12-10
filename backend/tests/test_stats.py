from fastapi import status

def test_stats_stocks(client):
    # Create devices with different statuses/locations
    client.post("/devices/", json={"serial_number": "D1", "current_location": "Bastia"}) # Stock by default
    
    # Move one to Service
    client.post("/actions/", json={
        "serial_number": "D1", 
        "action_type": "POSE", 
        "location": "Bastia"
    })
    
    # Create another in Stock
    client.post("/devices/", json={"serial_number": "D2", "current_location": "Ajaccio"})
    
    response = client.get("/stats/stocks")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Expect: Bastia/EN_SERVICE: 1, Ajaccio/STOCK: 1
    found_bastia = False
    for item in data:
        if item["location"] == "Bastia" and item["status"] == "EN_SERVICE":
            assert item["count"] == 1
            found_bastia = True
    assert found_bastia

def test_dashboard_history(client):
    client.post("/devices/", json={"serial_number": "D3"})
    client.post("/actions/", json={"serial_number": "D3", "action_type": "RECEPTION"})
    client.post("/actions/", json={"serial_number": "D3", "action_type": "TRANSFERT"})
    
    response = client.get("/dashboard/history")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    # Ensure DESC order (transfert most recent)
    assert data[0]["action_type"] == "TRANSFERT"
