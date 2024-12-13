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
def get_teams_by_match(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT team_id_a, team_id_b, team_a, team_b FROM euroleague_header WHERE game_id = %s", (game_id, ))
    team = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify({'team': team})

@admin_required
def get_players_by_team_season(team_id, season_code):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT euroleague_player_names.player_id, euroleague_player_names.player_name FROM euroleague_players LEFT JOIN euroleague_player_names ON euroleague_players.player_id = euroleague_player_names.player_id WHERE team_id = %s AND season_code = %s ORDER BY euroleague_player_names.player_name ASC", (team_id, season_code))
    players = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'players': players})

@admin_required
def panel_users_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT *, CASE WHEN role = 'U' THEN 'User' WHEN role = 'A' THEN 'Admin' ELSE 'Unknown' END AS role_detailed FROM users")
    users = cursor.fetchall()

    for user in users:
        user['data_attributes'] = ' '.join([f'data-{key}={value}' for key, value in user.items()])

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

@admin_required
def panel_box_scores_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT *, euroleague_box_score.player_id AS player_id, euroleague_box_score.team_id AS team_id FROM euroleague_box_score LEFT JOIN euroleague_player_names ON euroleague_box_score.player_id = euroleague_player_names.player_id LEFT JOIN euroleague_team_names ON euroleague_box_score.team_id = euroleague_team_names.team_id ORDER BY game_id, euroleague_box_score.team_id ASC LIMIT 100")
    box_scores = cursor.fetchall()

    for bx in box_scores:
        bx['data_attributes'] = ' '.join([f'data-{key}={value}' for key, value in bx.items()])

    cursor.execute("SELECT * FROM euroleague_header")
    matches = cursor.fetchall()
    cursor.execute("SELECT * FROM euroleague_player_names ORDER BY player_name ASC")
    player_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_box_scores.html", box_scores=box_scores, matches=matches, player_names=player_names)

@admin_required
def panel_box_scores_add():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']
    player_id = request.form['player_id']
    game_player_id = f"{game_id}_{player_id}"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_box_score WHERE game_player_id = %s", (game_player_id, ))
    bx_existing = cursor.fetchone()
    if bx_existing:
        flash("This box score already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for('panel_box_scores_page'))
    
    cursor.execute("DESCRIBE euroleague_box_score")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game_player_id'] = game_player_id
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    sql = f"""INSERT INTO euroleague_box_score ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Box score added successfully!", "success")
    return redirect(url_for('panel_box_scores_page'))

@admin_required
def panel_box_scores_update():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']
    player_id = request.form['player_id']
    game_player_id = request.form['game_player_id']
    new_game_player_id = f"{game_id}_{player_id}"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_box_score WHERE game_player_id = %s", (new_game_player_id, ))
    bx_existing = cursor.fetchone()
    if bx_existing and game_player_id != new_game_player_id:
        flash("The box score for that player in that game already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for('panel_box_scores_page'))

    cursor.execute("DESCRIBE euroleague_box_score")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game_player_id'] = game_player_id
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data])
    sql = f"""UPDATE euroleague_box_score SET {set_str} WHERE game_player_id = %(game_player_id)s"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Box score updated successfully!", "success")
    return redirect(url_for('panel_box_scores_page'))

@admin_required
def panel_box_scores_delete():
    game_player_id = request.form['game_player_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_box_score WHERE game_player_id = %s", (game_player_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Box score deleted successfully!", "success")
    return redirect(url_for('panel_box_scores_page'))
