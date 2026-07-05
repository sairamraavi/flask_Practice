"""Tests for the Flask student management app."""

import pytest

from app import app, mongo


@pytest.fixture
def client_fixture():
    """Create a test client and seed the student collection."""
    app.config["TESTING"] = True

    client = app.test_client()

    # Clean collection before every test
    with app.app_context():
        mongo.db.students.delete_many({})

        mongo.db.students.insert_one(
            {"name": "Test Student", "email": "test@student.com", "course": "Flask"}
        )

    yield client

    # Clean collection after every test
    with app.app_context():
        mongo.db.students.delete_many()


def test_home_page(client):
    """Verify the home page shows seeded students."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Test Student" in response.data


def test_add_student(client):
    """Verify a new student can be added through the form."""
    data = {"name": "New User", "email": "new@user.com", "course": "Python"}

    response = client.post("/add", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"New User" in response.data


def test_update_student(client):
    """Verify an existing student can be updated."""
    with app.app_context():
        student = mongo.db.students.find_one({"name": "Test Student"})
        student_id = str(student["_id"])

    data = {
        "name": "Updated Name",
        "email": "updated@student.com",
        "course": "Updated Course",
    }

    response = client.post(f"/update/{student_id}", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Updated Name" in response.data


def test_delete_student(client):
    """Verify an existing student can be deleted."""
    with app.app_context():
        student = mongo.db.students.find_one({"name": "Test Student"})
        student_id = str(student["_id"])

    response = client.get(f"/delete/{student_id}", follow_redirects=True)

    assert response.status_code == 200
    assert b"Test Student" not in response.data
