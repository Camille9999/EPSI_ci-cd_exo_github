import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.skipif(not os.getenv("GOOGLE_API_KEY"), reason="GOOGLE_API_KEY not found")
def test_generate_e2e_real_call():
    """
    Test E2E : Appelle la VRAIE API Google Gemini.
    Ce test consomme des crédits/quotas API.
    """

    prompt = "Quelle est la capitale de la France ? Réponds en un seul mot."
    expected_keyword = "Paris"

    response = client.post("/generate", json={"prompt": prompt})

    assert response.status_code == 200, f"Erreur API: {response.text}"
    json_data = response.json()
    assert "response" in json_data

    actual_response = json_data["response"].lower()

    assert expected_keyword.lower() in actual_response, \
        f"La réponse '{actual_response}' ne contient pas le mot clé '{expected_keyword}'"
