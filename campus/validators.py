"""Input validation helpers. Each returns a list of error messages (empty = valid)."""
import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REG_RE = re.compile(r"^[A-Za-z0-9\-]{3,20}$")


def is_valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def is_valid_time(value):
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except (TypeError, ValueError):
        return False


def validate_student(reg_no, name, department, email):
    errors = []
    if not REG_RE.match(reg_no or ""):
        errors.append("Register number must be 3-20 letters, digits or hyphens.")
    if not (name or "").strip():
        errors.append("Name is required.")
    if not (department or "").strip():
        errors.append("Department is required.")
    if not EMAIL_RE.match(email or ""):
        errors.append("Enter a valid email address.")
    return errors


def validate_booking(booked_by, purpose, date, start, end):
    errors = []
    if not (booked_by or "").strip():
        errors.append("Booked-by name is required.")
    if not (purpose or "").strip():
        errors.append("Purpose is required.")
    if not is_valid_date(date):
        errors.append("Date must be in YYYY-MM-DD format.")
    if not is_valid_time(start) or not is_valid_time(end):
        errors.append("Start and end times must be in HH:MM format.")
    elif start >= end:
        errors.append("End time must be after start time.")
    return errors


def validate_notice(title, body):
    errors = []
    if not (title or "").strip():
        errors.append("Title is required.")
    elif len(title) > 100:
        errors.append("Title must be 100 characters or fewer.")
    if not (body or "").strip():
        errors.append("Notice text is required.")
    return errors
