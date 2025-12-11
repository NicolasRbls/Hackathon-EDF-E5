from app import models, security

from app import models, security

def test_carton_capacity(client, admin_token):
    # Fill carton
    for i in range(4):
        r = client.post("/devices/", json={"serial_number": f"L-{i}", "num_carton": "CARTON-LIMIT"}, headers=admin_token)
        assert r.status_code == 201

    # Add 5th
    r = client.post("/devices/", json={"serial_number": "L-EXCESS", "num_carton": "CARTON-LIMIT"}, headers=admin_token)
    assert r.status_code == 400
    assert "Carton CARTON-LIMIT is full" in r.json()["detail"]
