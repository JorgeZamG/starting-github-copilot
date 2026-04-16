"""
Tests for the Mergington High School API

Uses the AAA (Arrange-Act-Assert) pattern to structure each test for clarity.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture to provide a TestClient instance for the FastAPI app"""
    return TestClient(app)


def test_get_activities(client):
    """Test retrieving all activities"""
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Class",
        "Music Band",
        "Robotics Club",
        "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert all(activity in data for activity in expected_activities)


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]
    assert activity_name in data["message"]


def test_signup_activity_not_found(client):
    """Test signup for a non-existent activity returns 404"""
    # Arrange
    invalid_activity_name = "NonExistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email(client):
    """Test signup with an email already signed up returns 400"""
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]
