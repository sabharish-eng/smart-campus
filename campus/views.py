import sqlite3
from datetime import date as date_cls
from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db
from .validators import (is_valid_date, validate_booking, validate_notice,
                         validate_student)

bp = Blueprint("campus", __name__)


# ---------- Dashboard ----------
@bp.route("/")
def index():
    db = get_db()
    counts = {
        "students": db.execute("SELECT COUNT(*) FROM students").fetchone()[0],
        "rooms": db.execute("SELECT COUNT(*) FROM rooms").fetchone()[0],
        "bookings": db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0],
        "notices": db.execute("SELECT COUNT(*) FROM notices").fetchone()[0],
    }
    latest = db.execute("SELECT * FROM notices ORDER BY id DESC LIMIT 3").fetchall()
    return render_template("index.html", counts=counts, latest=latest)


# ---------- Students ----------
@bp.route("/students", methods=["GET", "POST"])
def students():
    db = get_db()
    if request.method == "POST":
        f = {k: request.form.get(k, "").strip() for k in ("reg_no", "name", "department", "email")}
        errors = validate_student(**f)
        if errors:
            for e in errors:
                flash(e, "error")
        else:
            try:
                db.execute("INSERT INTO students (reg_no, name, department, email) VALUES (?,?,?,?)",
                           (f["reg_no"], f["name"], f["department"], f["email"]))
                db.commit()
                flash("Student added.", "success")
            except sqlite3.IntegrityError:
                flash("A student with this register number already exists.", "error")
        return redirect(url_for("campus.students"))
    rows = db.execute("SELECT * FROM students ORDER BY reg_no").fetchall()
    return render_template("students.html", students=rows)


@bp.post("/students/<int:student_id>/delete")
def delete_student(student_id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    flash("Student removed.", "success")
    return redirect(url_for("campus.students"))


# ---------- Attendance ----------
@bp.route("/attendance", methods=["GET", "POST"])
def attendance():
    db = get_db()
    day = request.values.get("date") or date_cls.today().isoformat()
    if not is_valid_date(day):
        flash("Invalid date. Showing today instead.", "error")
        day = date_cls.today().isoformat()

    students_list = db.execute("SELECT * FROM students ORDER BY reg_no").fetchall()

    if request.method == "POST":
        for s in students_list:
            status = request.form.get(f"status_{s['id']}", "Absent")
            if status not in ("Present", "Absent"):
                status = "Absent"
            db.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (?,?,?) "
                "ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status",
                (s["id"], day, status))
        db.commit()
        flash(f"Attendance saved for {day}.", "success")
        return redirect(url_for("campus.attendance", date=day))

    marked = {r["student_id"]: r["status"] for r in
              db.execute("SELECT student_id, status FROM attendance WHERE date = ?", (day,))}
    return render_template("attendance.html", students=students_list, marked=marked, day=day)


@bp.route("/attendance/report")
def attendance_report():
    rows = get_db().execute("""
        SELECT s.reg_no, s.name,
               COALESCE(SUM(a.status = 'Present'), 0) AS present,
               COUNT(a.id) AS total
        FROM students s LEFT JOIN attendance a ON a.student_id = s.id
        GROUP BY s.id ORDER BY s.reg_no
    """).fetchall()
    report = [{**dict(r), "percent": round(100 * r["present"] / r["total"], 1) if r["total"] else None}
              for r in rows]
    return render_template("report.html", report=report)


# ---------- Rooms & bookings ----------
@bp.route("/rooms", methods=["GET", "POST"])
def rooms():
    db = get_db()
    if request.method == "POST":
        room_id = request.form.get("room_id", "")
        booked_by = request.form.get("booked_by", "").strip()
        purpose = request.form.get("purpose", "").strip()
        day = request.form.get("date", "")
        start = request.form.get("start_time", "")
        end = request.form.get("end_time", "")

        errors = validate_booking(booked_by, purpose, day, start, end)
        room = db.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone() \
            if room_id.isdigit() else None
        if room is None:
            errors.append("Please choose a valid room.")

        if not errors:
            clash = db.execute(
                "SELECT 1 FROM bookings WHERE room_id = ? AND date = ? "
                "AND start_time < ? AND end_time > ?",
                (room["id"], day, end, start)).fetchone()
            if clash:
                errors.append("That room is already booked during this time slot.")

        if errors:
            for e in errors:
                flash(e, "error")
        else:
            db.execute("INSERT INTO bookings (room_id, booked_by, purpose, date, start_time, end_time) "
                       "VALUES (?,?,?,?,?,?)", (room["id"], booked_by, purpose, day, start, end))
            db.commit()
            flash("Room booked.", "success")
        return redirect(url_for("campus.rooms"))

    room_rows = db.execute("SELECT * FROM rooms ORDER BY name").fetchall()
    bookings = db.execute("""
        SELECT b.*, r.name AS room_name FROM bookings b JOIN rooms r ON r.id = b.room_id
        ORDER BY b.date, b.start_time""").fetchall()
    return render_template("rooms.html", rooms=room_rows, bookings=bookings)


@bp.post("/bookings/<int:booking_id>/delete")
def delete_booking(booking_id):
    db = get_db()
    db.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    db.commit()
    flash("Booking cancelled.", "success")
    return redirect(url_for("campus.rooms"))


# ---------- Notices ----------
@bp.route("/notices", methods=["GET", "POST"])
def notices():
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        errors = validate_notice(title, body)
        if errors:
            for e in errors:
                flash(e, "error")
        else:
            db.execute("INSERT INTO notices (title, body) VALUES (?,?)", (title, body))
            db.commit()
            flash("Notice posted.", "success")
        return redirect(url_for("campus.notices"))
    rows = db.execute("SELECT * FROM notices ORDER BY id DESC").fetchall()
    return render_template("notices.html", notices=rows)


@bp.post("/notices/<int:notice_id>/delete")
def delete_notice(notice_id):
    db = get_db()
    db.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
    db.commit()
    flash("Notice deleted.", "success")
    return redirect(url_for("campus.notices"))
