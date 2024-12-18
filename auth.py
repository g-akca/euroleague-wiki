from flask import current_app, render_template, request, session, redirect, url_for, flash, jsonify
from db import get_db_connection
from markupsafe import Markup
from functools import wraps
from datetime import timedelta
import bcrypt

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == "A":
            return f(*args, **kwargs)
        else:
            return redirect(url_for("restricted"))
    return wrap

def refresh_session_data():
    if session.get('loggedin') == True:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'], ))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']
            session['team_supported'] = user['team_supported']
        else:
            session.clear()

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username, ))
        found_user = cursor.fetchone()
        cursor.close()
        connection.close()

        if not found_user:
            message = Markup(f"This username does not exist! <a href='{ url_for('signup') }' class='alert-link'>Try signing up?</a>")
            flash(message, "danger")
            return render_template("login.html")
        elif bcrypt.checkpw(password.encode('UTF-8'), found_user['hashed_password'].encode('UTF-8')):
            session['loggedin'] = True
            session['user_id'] = found_user['user_id']

            if remember == 'True':
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(days=20)
            else:
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(days=1)

            flash("Welcome back to Euroleague Wiki!", "success")
            return redirect(url_for("home_page"))
        else:
            flash("Incorrect password!", "danger")
            return render_template("login.html")
        
    # GET request
    else:
        if session.get('loggedin') == True:
            return redirect(url_for("restricted"))
        else:
            return render_template("login.html")

def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        team_supported = request.form['team_supported']
        remember = request.form.get('remember')

        if team_supported == "":
            team_supported = None

        if password != password2:
            flash("Passwords did not match, please try again!", "danger")
            return render_template("signup.html")
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
        user_existing = cursor.fetchone()

        if user_existing:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username, ))
            found_username = cursor.fetchone()
            cursor.close()
            connection.close()

            if found_username:
                message = Markup(f"This username is already in use! <a href='{ url_for('login') }' class='alert-link'>Try logging in?</a>")
                flash(message, "danger")
            else:
                message = Markup(f"This email address is already in use! <a href='{ url_for('login') }' class='alert-link'>Try logging in?</a>")
                flash(message, "danger")

            return render_template("signup.html")
        else:
            hashed_pw = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            cursor.execute('INSERT INTO users (username, email, hashed_password, team_supported) VALUES (%s, %s, %s, %s)', (username, email, hashed_pw, team_supported))
            connection.commit()
            cursor.execute('SELECT * FROM users WHERE username = %s AND email = %s', (username, email))
            new_account = cursor.fetchone()
            cursor.close()
            connection.close()

            session['loggedin'] = True
            session['user_id'] = new_account['user_id']

            if remember == 'True':
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(days=20)
            else:
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(days=1)

            flash("Successfully signed up!", "success")
            return redirect(url_for("home_page"))
    else:
        if session.get('loggedin') == True:
            return redirect(url_for("restricted"))
        else:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
            team_names = cursor.fetchall()
            cursor.close()
            connection.close()

            return render_template("signup.html", team_names=team_names)

def logout():
    if session.get('loggedin') == True:
        session.clear()
        flash("Logged out successfully!", "success")
        return redirect("/login")
    else:
        return redirect(url_for("restricted"))
    
def get_teams():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(team_names)

def update_account():
    user_id = session['user_id']
    newUsername = request.form['username']
    newEmail = request.form['email']
    currentPw = request.form['password']
    newPw = request.form['passwordNew']
    team_supported = request.form['team_supported']

    if team_supported == "":
        team_supported = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id, ))
    current_user = cursor.fetchone()
    cursor.close()
    connection.close()

    if bcrypt.checkpw(currentPw.encode('UTF-8'), current_user['hashed_password'].encode('UTF-8')):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if newPw != '':
            hashed_newPw = bcrypt.hashpw(newPw.encode('UTF-8'), bcrypt.gensalt())
            cursor.execute('UPDATE users SET username = %s, email = %s, hashed_password = %s, team_supported = %s WHERE user_id = %s', (newUsername, newEmail, hashed_newPw, team_supported, user_id))
        else:
            cursor.execute('UPDATE users SET username = %s, email = %s, team_supported = %s WHERE user_id = %s', (newUsername, newEmail, team_supported, user_id))

        connection.commit()
        cursor.close()
        connection.close()

        flash("Account details updated successfully!", "success")
        return redirect(url_for("home_page"))
    else:
        flash("You have entered your current password wrong, please try again!", "danger")
        return redirect(url_for("home_page"))

def restricted():
    return render_template("403.html")

def not_found():
    return render_template("404.html")
