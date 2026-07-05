"""Flask application for managing student records."""

import os

import certifi
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo

# Load env vars
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")

# Use certifi CA bundle explicitly for cross-platform TLS reliability
# (notably fixes common macOS certificate verification failures).
mongo = PyMongo(app, tlsCAFile=certifi.where())


@app.route("/")
def index():
    """Render the home page with the list of students."""
    students = mongo.db.students.find()
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    """Add a new student through the form or redirect to the home page."""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        mongo.db.students.insert_one({"name": name, "email": email, "course": course})
        return redirect(url_for("index"))
    return render_template("add_student.html")


@app.route("/update/<student_id>", methods=["GET", "POST"])
def update_student(student_id):
    """Update a student's details or display the edit form."""
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if request.method == "POST":
        new_name = request.form["name"]
        new_email = request.form["email"]
        new_course = request.form["course"]
        mongo.db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": {"name": new_name, "email": new_email, "course": new_course}},
        )
        return redirect(url_for("index"))
    return render_template("update_student.html", student=student)


@app.route("/delete/<student_id>")
def delete_student(student_id):
    """Delete a student and redirect back to the home page."""
    mongo.db.students.delete_one({"_id": ObjectId(student_id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
