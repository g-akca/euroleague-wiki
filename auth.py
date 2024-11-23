from flask import render_template, request, session, redirect, url_for, flash
from db import get_db_connection

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        found_user = cursor.fetchone()
        if found_user:
            cursor.close()
            connection.close()
            session['loggedin'] = True
            session['user_id'] = found_user['user_id']
            session['username'] = found_user['username']
            session['email'] = found_user['email']
            session['role'] = found_user['role']
            flash("Successfully logged in!")
            return redirect(url_for("home_page"))
        else:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username, ))
            found_username = cursor.fetchone()
            cursor.close()
            connection.close()
            if found_username:
                flash("Incorrect password!")
            else:
                flash("This username does not exist!")
            return render_template("login.html")
    else:
        if session.get('loggedin') == True:
            return redirect(url_for("home_page")) # Sends user to homepage if already logged in. Might add a restricted page warning instead
        else:
            return render_template("login.html")

def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
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
                flash("This username is already in use!")
            else:
                flash("This email address is already in use!")
            return render_template("signup.html")
        else:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            connection.commit()
            cursor.execute('SELECT * FROM users WHERE username = %s AND email = %s', (username, email))
            new_account = cursor.fetchone()
            cursor.close()
            connection.close()
            session['loggedin'] = True
            session['user_id'] = new_account['user_id']
            session['username'] = new_account['username']
            session['email'] = new_account['email']
            session['role'] = new_account['role']
            flash("Successfully signed up!")
            return redirect(url_for("home_page"))
    else:
        if session.get('loggedin') == True:
            return redirect(url_for("home_page")) # Sends user to homepage if already logged in. Might add a restricted page warning instead
        else:
            return render_template("signup.html")

def logout():
    if session.get('loggedin') == True:
        session.pop('loggedin', None)
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('email', None)
        session.pop('role', None)
        flash("Logged out successfully!")
        return redirect("login")
    else:
        return redirect(url_for("home_page")) # Sends user to homepage if not logged in. Might add a restricted page warning instead
    