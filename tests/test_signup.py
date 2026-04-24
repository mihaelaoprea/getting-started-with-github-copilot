"""Tests for POST /activities/{activity_name}/signup endpoint."""


def test_signup_successful(client):
    """Test successful signup for an activity."""
    # Arrange: Choose an existing activity and a new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup endpoint
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Response status is 200
    assert response.status_code == 200

    # Assert: Response contains success message
    result = response.json()
    assert "message" in result
    assert f"Signed up {email} for {activity_name}" in result["message"]

    # Assert: Participant was added to the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_non_existent_activity(client):
    """Test signup for a non-existent activity returns 404."""
    # Arrange: Use an invalid activity name
    invalid_activity = "NonExistentActivity"
    email = "student@mergington.edu"

    # Act: Make POST request to signup endpoint
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

    # Assert: Response status is 404
    assert response.status_code == 404

    # Assert: Response contains appropriate error message
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_signup_duplicate_registration(client):
    """Test that duplicate signup for same activity returns 400."""
    # Arrange: First, sign up a student
    activity_name = "Programming Class"
    email = "duplicatestudent@mergington.edu"

    # Sign up once (should succeed)
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    # Act: Attempt to sign up the same student again
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Second signup returns 400
    assert second_response.status_code == 400

    # Assert: Response contains appropriate error message
    result = second_response.json()
    assert "detail" in result
    assert "Student already signed up" in result["detail"]