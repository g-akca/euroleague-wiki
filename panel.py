from flask import render_template, request, jsonify, flash, redirect, url_for
from db import get_db_connection
from auth import admin_required
import bcrypt

@admin_required
def get_counts():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(user_id) AS users_count FROM users")
    users_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(team_id) AS teams_count FROM euroleague_team_names")
    teams_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(player_id) AS players_count FROM euroleague_player_names")
    players_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(game_id) AS matches_count FROM euroleague_header")
    matches_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(game_id) AS comparisons_count FROM euroleague_comparison")
    comparisons_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(game_player_id) AS box_scores_count FROM euroleague_box_score")
    box_scores_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(game_play_id) AS plays_count FROM euroleague_play_by_play")
    plays_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(primary_point_id) AS points_count FROM euroleague_points")
    points_count = cursor.fetchone()

    cursor.close()
    connection.close()
    return jsonify({
        "counts": [ users_count['users_count'],
                    teams_count['teams_count'],
                    players_count['players_count'],
                    matches_count['matches_count'],
                    comparisons_count['comparisons_count'],
                    box_scores_count['box_scores_count'],
                    points_count['points_count'],
                    plays_count['plays_count']
                    ]})

@admin_required
def panel_users_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT *, CASE WHEN role = 'U' THEN 'User' WHEN role = 'A' THEN 'Admin' ELSE 'Unknown' END AS role_detailed FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_users.html", users=users, team_names=team_names)

@admin_required
def panel_users_add():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    team_supported = request.form['team_supported']
    role = request.form['role']
    hashed_pw = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

    if team_supported == "":
        team_supported = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("INSERT INTO users (username, email, hashed_password, role, team_supported) VALUES (%s, %s, %s, %s, %s)", (username, email, hashed_pw, role, team_supported))
    connection.commit()
    cursor.close()
    connection.close()

    flash("User created successfully!", "success")
    return redirect(url_for('panel_users_page'))

@admin_required
def panel_users_update():
    user_id = request.form['user_id']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    team_supported = request.form['team_supported']
    role = request.form['role']

    if team_supported == "":
        team_supported = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if password != "":
        hashed_pw = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET username = %s, email = %s, hashed_password = %s, role = %s, team_supported = %s WHERE user_id = %s", (username, email, hashed_pw, role, team_supported, user_id))
    else:
        cursor.execute("UPDATE users SET username = %s, email = %s, role = %s, team_supported = %s WHERE user_id = %s", (username, email, role, team_supported, user_id))
    connection.commit()
    cursor.close()
    connection.close()

    flash("User updated successfully!", "success")
    return redirect(url_for('panel_users_page'))

@admin_required
def panel_users_delete():
    user_id = request.form['user_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for('panel_users_page'))

@admin_required
def panel_teams_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_teams.html", team_names=team_names)
