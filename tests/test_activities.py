"""
Tests for the GET /activities endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test cases for retrieving activities."""
    
    def test_get_all_activities_returns_success(self, client):
        """
        Test that GET /activities returns all activities successfully.
        
        Arrange: No setup needed, activities already loaded via fixture
        Act: Call GET /activities
        Assert: Response status is 200 and contains expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Debate Club",
            "Science Olympiad",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Music Band",
            "Art Studio",
            "Drama Club"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_activity_structure_is_valid(self, client):
        """
        Test that each activity has the correct structure and data types.
        
        Arrange: No setup needed
        Act: Call GET /activities
        Assert: Each activity has required fields with correct types
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity in data.items():
            assert isinstance(activity, dict), f"{activity_name} should be a dict"
            for field in required_fields:
                assert field in activity, f"{activity_name} missing field: {field}"
            
            # Verify field types
            assert isinstance(activity["description"], str)
            assert isinstance(activity["schedule"], str)
            assert isinstance(activity["max_participants"], int)
            assert isinstance(activity["participants"], list)
            assert all(isinstance(p, str) for p in activity["participants"])
    
    def test_participants_count_matches_data(self, client):
        """
        Test that participant count is accurate in the response.
        
        Arrange: No setup needed
        Act: Call GET /activities
        Assert: Each activity has correct participant data
        """
        # Arrange
        expected_participants = {
            "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
            "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, expected_participants_list in expected_participants.items():
            assert data[activity_name]["participants"] == expected_participants_list
            assert len(data[activity_name]["participants"]) == len(expected_participants_list)
