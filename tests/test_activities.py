"""Tests for GET /activities endpoint."""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure."""
    # Arrange: No specific setup needed as activities are predefined in app

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Response status is 200
    assert response.status_code == 200

    # Assert: Response contains all 9 activities
    activities = response.json()
    assert len(activities) == 9

    # Assert: Each activity has the expected structure
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
    ]
    assert set(activities.keys()) == set(expected_activities)

    # Assert: Each activity has required fields
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participant_counts(client):
    """Test that participant counts are correct for each activity."""
    # Arrange: No specific setup needed

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Response is successful
    assert response.status_code == 200

    activities = response.json()

    # Assert: Specific participant counts match expected values
    expected_counts = {
        "Chess Club": 2,  # michael@mergington.edu, daniel@mergington.edu
        "Programming Class": 2,  # emma@mergington.edu, sophia@mergington.edu
        "Gym Class": 2,  # john@mergington.edu, olivia@mergington.edu
        "Basketball Team": 1,  # james@mergington.edu
        "Tennis Club": 1,  # isabella@mergington.edu
        "Art Studio": 2,  # lucas@mergington.edu, ava@mergington.edu
        "Drama Club": 1,  # noah@mergington.edu
        "Debate Team": 2,  # mia@mergington.edu, ethan@mergington.edu
        "Science Club": 1,  # charlotte@mergington.edu
    }

    for activity_name, expected_count in expected_counts.items():
        assert len(activities[activity_name]["participants"]) == expected_count