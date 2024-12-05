from flask import render_template, request, session, redirect, url_for, flash
from db import get_db_connection

# Might switch to Flask Login instead of sessions

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
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        found_user = cursor.fetchone()

        if found_user:
            cursor.close()
            connection.close()
            session['loggedin'] = True
            session['user_id'] = found_user['user_id']

            if remember == 'True':
                session.permanent = True # Set session to permanent if "Remember me" is checked

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
        password2 = request.form['password2']
        team_supported = request.form['team_supported']
        if team_supported == "":
            team_supported = None
        remember = request.form.get('remember')

        if password != password2:
            flash("Passwords did not match, please try again!")
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
                flash("This username is already in use!")
            else:
                flash("This email address is already in use!")

            return render_template("signup.html")
        else:
            cursor.execute('INSERT INTO users (username, email, password, team_supported) VALUES (%s, %s, %s, %s)', (username, email, password, team_supported))
            connection.commit()
            cursor.execute('SELECT * FROM users WHERE username = %s AND email = %s', (username, email))
            new_account = cursor.fetchone()
            cursor.close()
            connection.close()

            session['loggedin'] = True
            session['user_id'] = new_account['user_id']

            if remember == 'True':
                session.permanent = True # Set session to permanent if "Remember me" is checked

            flash("Successfully signed up!")
            return redirect(url_for("home_page"))
    else:
        if session.get('loggedin') == True:
            return redirect(url_for("home_page")) # Sends user to homepage if already logged in. Might add a restricted page warning instead
        else:
            return render_template("signup.html")

def logout():
    if session.get('loggedin') == True:
        session.clear()
        flash("Logged out successfully!")
        return redirect("login")
    else:
        return redirect(url_for("home_page")) # Sends user to homepage if not logged in. Might add a restricted page warning instead
    
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

    if currentPw == current_user['password']:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if newPw != '':
            cursor.execute('UPDATE users SET username = %s, email = %s, password = %s, team_supported = %s WHERE user_id = %s', (newUsername, newEmail, newPw, team_supported, user_id))
        else:
            cursor.execute('UPDATE users SET username = %s, email = %s, team_supported = %s WHERE user_id = %s', (newUsername, newEmail, team_supported, user_id))

        connection.commit()
        cursor.close()
        connection.close()
        flash("Account details updated successfully!")
        return redirect(url_for("home_page"))
    else:
        flash("You have entered your current password wrong, please try again!")
        return redirect(url_for("home_page"))
