# CONTAINS ALL THE LOGIN STUFF
from flask import Blueprint, render_template, request, flash
import re

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    data = request.form
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<h1>logout page</h1>"

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # simple form verification
        emailregex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(emailregex, email):
            flash("Email not valid good sir!", category='error')
        elif len(firstName) < 3:
            flash("firstName too short mydude!", category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account Created', category='success')

    return render_template("signup.html")