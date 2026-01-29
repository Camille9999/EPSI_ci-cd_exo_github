import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest

os.environ["GOOGLE_API_KEY"] = "fake_key_for_testing"

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.genai.Client")
@pytest.mark.skipif(os.getenv("SKIP_API_TESTS") == "true", reason="SKIP_API_TESTS set")
def test_generate_text_mock(mock_client_class):
    """Test qui simule l'appel à Gemini sans internet"""

    mock_instance = mock_client_class.return_value
    mock_response = MagicMock()
    mock_response.text = "Ceci est une réponse simulée."

    mock_instance.models.generate_content.return_value = mock_response

    response = client.post("/generate", json={"prompt": "Bonjour"})

    if response.status_code != 200:
        print("Erreur API:", response.json())

    assert response.status_code == 200
    assert response.json() == {"response": "Ceci est une réponse simulée."}
