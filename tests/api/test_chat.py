from unittest.mock import patch


def test_chat_endpoint(client):
    payload = {
        "message": "Hello",
        "session_id": "test-session"
    }

    headers = {"X-API-Key": "dev-key"}

    with patch("orchestrator.pipeline.run_pipeline") as mock_pipeline:
        mock_pipeline.return_value = {
            "text": "Hello there!",
            "emotion": "happy",
            "video_url": "/fake/video.mp4",
        }

        response = client.post(
            "/chat/avatar",
            json=payload,
            headers=headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["emotion"] == "happy"
    assert "video_url" in data
