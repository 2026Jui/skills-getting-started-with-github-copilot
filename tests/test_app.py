import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    email = "testuser@example.com"
    activity = "Basketball Team"
    # Ensure not already registered
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Signup
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    # Duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400
    # Unregister
    r3 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert r3.status_code == 200
    # Unregister again should fail
    r4 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert r4.status_code == 404
