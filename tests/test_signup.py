"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignup:
    """Test cases for signing up for activities."""
    
    def test_signup_success(self, client):
        """
        Test successful signup for an activity.
        
        Arrange: Prepare a new email and activity that exists
        Act: Call POST /activities/{activity}/signup?email={email}
        Assert: Response is 200, message contains confirmation
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """
        Test that signup actually adds the participant to the activity list.
        
        Arrange: Prepare a new email
        Act: Sign up and then retrieve activities
        Assert: The participant is in the activity's participants list
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newcoder@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        
        # Assert
        activity_data = response.json()[activity_name]
        assert email in activity_data["participants"]
    
    def test_signup_fails_nonexistent_activity(self, client):
        """
        Test signup fails with 404 when activity doesn't exist.
        
        Arrange: Use a non-existent activity name
        Act: Call POST with invalid activity
        Assert: Response is 404 with "not found" message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_fails_duplicate_participant(self, client):
        """
        Test signup fails with 400 when student already signed up.
        
        Arrange: Use an email already registered for the activity
        Act: Call POST with existing participant
        Assert: Response is 400 with "already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_participant_count_increases(self, client):
        """
        Test that participant count increases after successful signup.
        
        Arrange: Get initial participant count
        Act: Sign up a new participant
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Debate Club"
        email = "newdebater@mergington.edu"
        
        # Get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
    
    def test_signup_multiple_participants(self, client):
        """
        Test that multiple different participants can sign up for same activity.
        
        Arrange: Prepare multiple new emails
        Act: Sign up multiple different participants
        Assert: All are successfully added
        """
        # Arrange
        activity_name = "Art Studio"
        new_emails = ["artist1@mergington.edu", "artist2@mergington.edu", "artist3@mergington.edu"]
        
        # Act
        for email in new_emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            # Assert each signup succeeds
            assert response.status_code == 200
        
        # Assert all are in the activity
        final_response = client.get("/activities")
        participants = final_response.json()[activity_name]["participants"]
        for email in new_emails:
            assert email in participants
