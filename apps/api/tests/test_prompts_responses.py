from datetime import datetime, timedelta, timezone


def create_user(client, whatsapp_id="5491122334488"):
    payload = {
        "whatsapp_id": whatsapp_id,
        "name": "Lucia",
        "goal": "academic",
        "timezone": "America/Bogota",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_and_list_prompts(client):
    user = create_user(client)
    now = datetime(2026, 2, 1, 9, 0, 0, tzinfo=timezone.utc)
    later = now + timedelta(hours=4)

    prompt_payloads = [
        {"content": "Prompt temprano", "scheduled_for": now.isoformat().replace("+00:00", "Z")},
        {"content": "Prompt tarde", "scheduled_for": later.isoformat().replace("+00:00", "Z")},
    ]

    for payload in prompt_payloads:
        response = client.post(f"/users/{user['id']}/prompts", json=payload)
        assert response.status_code == 201

    list_response = client.get(f"/users/{user['id']}/prompts")

    assert list_response.status_code == 200
    rows = list_response.json()
    assert len(rows) == 2
    assert rows[0]["content"] == "Prompt tarde"
    assert rows[1]["content"] == "Prompt temprano"


def test_create_response(client):
    user = create_user(client, whatsapp_id="5491122334499")
    scheduled_for = datetime(2026, 2, 1, 9, 0, 0, tzinfo=timezone.utc)

    prompt_response = client.post(
        f"/users/{user['id']}/prompts",
        json={
            "content": "Escribe una frase con la palabra 'ambiguo'",
            "scheduled_for": scheduled_for.isoformat().replace("+00:00", "Z"),
        },
    )
    assert prompt_response.status_code == 201
    prompt_id = prompt_response.json()["id"]

    response_payload = {
        "prompt_id": prompt_id,
        "content": "El informe es ambiguo y requiere mas datos.",
    }
    response = client.post(f"/users/{user['id']}/responses", json=response_payload)

    assert response.status_code == 201
    created = response.json()
    assert created["prompt_id"] == prompt_id
    assert created["is_valid"] is False

    list_response = client.get(f"/users/{user['id']}/responses")

    assert list_response.status_code == 200
    rows = list_response.json()
    assert len(rows) == 1
    assert rows[0]["content"] == response_payload["content"]
