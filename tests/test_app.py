import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange
    # (No setup needed for in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    email = "testuser@example.com"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Cleanup
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

def test_signup_duplicate():
    # Arrange
    email = "testuser2@example.com"
    activity = "Chess Club"
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

    # Cleanup
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

def test_unregister_from_activity():
    # Arrange
    email = "testuser3@example.com"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

    # Act again: try to unregister again (should fail)
    response2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response2.status_code == 404
    assert response2.json()["detail"] == "Participant not found"
