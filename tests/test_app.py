import pytest
from campus import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def add_student(client, reg="CS101", email="a@b.com"):
    return client.post("/students", data={"reg_no": reg, "name": "Asha",
                       "department": "CSE", "email": email}, follow_redirects=True)


def test_dashboard_loads(client):
    assert client.get("/").status_code == 200


def test_add_student_success(client):
    assert b"Student added" in add_student(client).data


def test_add_student_invalid_email(client):
    assert b"valid email" in add_student(client, email="bad").data


def test_duplicate_register_number(client):
    add_student(client)
    assert b"already exists" in add_student(client).data


def test_attendance_saved_and_reported(client):
    add_student(client)
    client.post("/attendance", data={"date": "2025-01-10", "status_1": "Present"})
    client.post("/attendance", data={"date": "2025-01-11", "status_1": "Absent"})
    assert b"50.0%" in client.get("/attendance/report").data


def test_invalid_attendance_date_does_not_crash(client):
    assert client.get("/attendance?date=garbage").status_code == 200


def book(client, start, end):
    return client.post("/rooms", data={"room_id": "1", "booked_by": "Dr. Ravi", "purpose": "Class",
                       "date": "2025-02-01", "start_time": start, "end_time": end},
                       follow_redirects=True)


def test_booking_success(client):
    assert b"Room booked" in book(client, "10:00", "11:00").data


def test_booking_conflict_rejected(client):
    book(client, "10:00", "11:00")
    assert b"already booked" in book(client, "10:30", "11:30").data


def test_adjacent_booking_allowed(client):
    book(client, "10:00", "11:00")
    assert b"Room booked" in book(client, "11:00", "12:00").data


def test_booking_end_before_start(client):
    assert b"after start" in book(client, "12:00", "11:00").data


def test_notice_post_and_validation(client):
    ok = client.post("/notices", data={"title": "Holiday", "body": "Tomorrow off"}, follow_redirects=True)
    assert b"Notice posted" in ok.data
    bad = client.post("/notices", data={"title": "", "body": ""}, follow_redirects=True)
    assert b"Title is required" in bad.data
