def create_user(client, whatsapp_id="5491122334477"):
    payload = {
        "whatsapp_id": whatsapp_id,
        "name": "Mario",
        "goal": "creative",
        "timezone": "America/Montevideo",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    return response.json()


def test_add_and_list_words(client):
    user = create_user(client)

    add_payload = {"words": ["Ambiguo", "perspicaz", "  "]}
    add_response = client.post(f"/users/{user['id']}/words", json=add_payload)

    assert add_response.status_code == 201
    created = add_response.json()["created"]
    created_texts = {row["text"] for row in created}
    assert created_texts == {"ambiguo", "perspicaz"}

    list_response = client.get(f"/users/{user['id']}/words")

    assert list_response.status_code == 200
    rows = list_response.json()
    assert len(rows) == 2
    assert {row["text"] for row in rows} == {"ambiguo", "perspicaz"}
