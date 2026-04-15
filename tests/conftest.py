"""
Pytest configuration and fixtures for the activities API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for API testing."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to initial state before each test.
    This ensures tests don't affect each other due to in-memory data.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop critical thinking and public speaking skills through competitive debate",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science competitions and conduct experimental research",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the school basketball team and compete in regional tournaments",
            "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "marcus@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Play instruments and perform in school concerts and events",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu", "henry@mergington.edu"]
        },
        "Art Studio": {
            "description": "Learn painting, drawing, and other visual art techniques",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["natalie@mergington.edu", "ryan@mergington.edu"]
        }
    }
    
    # Clear current activities
    activities.clear()
    
    # Restore original state
    for activity_name, activity_data in original_activities.items():
        activities[activity_name] = activity_data.copy()
        activities[activity_name]["participants"] = activity_data["participants"].copy()
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
