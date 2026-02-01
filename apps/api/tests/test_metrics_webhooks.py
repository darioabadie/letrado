from datetime import datetime, timezone


def create_user(client, whatsapp_id="5491122334500"):
    payload = {
        "whatsapp_id": whatsapp_id,
        "name": "Sofia",
        "goal": "professional",
        "timezone": "America/Mexico_City",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    return response.json()


def test_get_ttr_metric_not_found(client):
    user = create_user(client)

    response = client.get(f"/users/{user['id']}/metrics/ttr")

    assert response.status_code == 404
    assert response.json()["detail"] == "ttr metric not found"


def test_whatsapp_webhook_accepts_payload(client):
    payload = {
        "from_id": "5491122334455",
        "message": "Hola, esta es mi respuesta",
        "timestamp": datetime(2026, 2, 1, 9, 10, 0, tzinfo=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
    }

    response = client.post("/webhooks/whatsapp", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}
