"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""


def test_unregister_successful(client):
    """Test successful unregister from an activity."""
    # Arrange: First sign up a participant, then unregister them
    activity_name = "Gym Class"
    email = "tempstudent@mergington.edu"

    # Sign up the participant
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    # Verify they are signed up
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]

    # Act: Make DELETE request to unregister endpoint
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert: Response status is 200
    assert response.status_code == 200

    # Assert: Response contains success message
    result = response.json()
    assert "message" in result
    assert f"Unregistered {email} from {activity_name}" in result["message"]

    # Assert: Participant was removed from the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_non_existent_activity(client):
    """Test unregister from a non-existent activity returns 404."""
    # Arrange: Use an invalid activity name
    invalid_activity = "NonExistentActivity"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister endpoint
    response = client.delete(f"/activities/{invalid_activity}/participants/{email}")

    # Assert: Response status is 404
    assert response.status_code == 404

    # Assert: Response contains appropriate error message
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_unregister_non_existent_participant(client):
    """Test unregister of a participant not signed up returns 404."""
    # Arrange: Use valid activity but email not registered
    activity_name = "Tennis Club"
    unregistered_email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister endpoint
    response = client.delete(f"/activities/{activity_name}/participants/{unregistered_email}")

    # Assert: Response status is 404
    assert response.status_code == 404

    # Assert: Response contains appropriate error message
    result = response.json()
    assert "detail" in result
    assert "Participant not found" in result["detail"]