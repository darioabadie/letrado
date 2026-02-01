def create_user(client, whatsapp_id="5491122334455"):
    payload = {
        "whatsapp_id": whatsapp_id,
        "name": "Ana",
        "goal": "professional",
        "timezone": "America/Argentina/Buenos_Aires",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_and_get_user(client):
    user = create_user(client)

    get_response = client.get(f"/users/{user['id']}")

    assert get_response.status_code == 200
    payload = get_response.json()
    assert payload["id"] == user["id"]
    assert payload["whatsapp_id"] == "5491122334455"
    assert payload["goal"] == "professional"


def test_update_user(client):
    user = create_user(client, whatsapp_id="5491122334466")

    update_payload = {
        "name": "Ana B.",
        "goal": "academic",
        "timezone": "America/Santiago",
    }
    update_response = client.patch(f"/users/{user['id']}", json=update_payload)

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "Ana B."
    assert updated["goal"] == "academic"
    assert updated["timezone"] == "America/Santiago"
