"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestParticipantRemoval:
    """Test cases for removing participants from activities."""
    
    def test_remove_participant_success(self, client):
        """
        Test successful removal of a participant from an activity.
        
        Arrange: Use an existing participant
        Act: Call DELETE /activities/{activity}/participants/{email}
        Assert: Response is 200, message confirms removal
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_remove_participant_from_activity_list(self, client):
        """
        Test that participant is actually removed from activity's list.
        
        Arrange: Use an existing participant
        Act: Remove participant and retrieve activities
        Assert: Participant is no longer in the activity
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert email not in participants
    
    def test_remove_participant_fails_nonexistent_activity(self, client):
        """
        Test removal fails with 404 when activity doesn't exist.
        
        Arrange: Use a non-existent activity name
        Act: Call DELETE with invalid activity
        Assert: Response is 404
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_participant_fails_participant_not_found(self, client):
        """
        Test removal fails with 404 when participant not in activity.
        
        Arrange: Use an email not registered for the activity
        Act: Call DELETE with non-existent participant
        Assert: Response is 404 with "Participant not found" message
        """
        # Arrange
        activity_name = "Debate Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    def test_remove_participant_decreases_count(self, client):
        """
        Test that participant count decreases after successful removal.
        
        Arrange: Get initial participant count
        Act: Remove a participant
        Assert: Participant count decreased by 1
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "james@mergington.edu"
        
        # Get initial count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        assert updated_count == initial_count - 1
    
    def test_remove_multiple_participants(self, client):
        """
        Test that multiple participants can be removed from same activity.
        
        Arrange: Use an activity with multiple participants
        Act: Remove multiple participants one by one
        Assert: All are successfully removed
        """
        # Arrange
        activity_name = "Music Band"
        emails_to_remove = ["grace@mergington.edu", "henry@mergington.edu"]
        
        # Act
        for email in emails_to_remove:
            response = client.delete(f"/activities/{activity_name}/participants/{email}")
            # Assert each removal succeeds
            assert response.status_code == 200
        
        # Assert all are removed from the activity
        final_response = client.get("/activities")
        participants = final_response.json()[activity_name]["participants"]
        for email in emails_to_remove:
            assert email not in participants
    
    def test_remove_and_readd_participant(self, client):
        """
        Test that a removed participant can be added back.
        
        Arrange: Use an existing participant
        Act: Remove participant, then sign them up again
        Assert: Participant is successfully re-added
        """
        # Arrange
        activity_name = "Art Studio"
        email = "maya@mergington.edu"
        
        # Act & Assert: Remove
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response_after_removal = client.get("/activities")
        assert email not in response_after_removal.json()[activity_name]["participants"]
        
        # Act & Assert: Re-add
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
        
        response_after_readd = client.get("/activities")
        assert email in response_after_readd.json()[activity_name]["participants"]
