from flask import render_template, request, jsonify, flash, redirect, url_for
from db import get_db_connection
from auth import admin_required
import bcrypt

# Needed for panel sidemenu
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

# Needed for populating Box Scores team dropdown
@admin_required
def get_teams_by_match(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT t1.team_name AS team_a, t2.team_name AS team_b, team_id_a, team_id_b FROM euroleague_header h LEFT JOIN euroleague_team_names t1 ON h.team_id_a = t1.team_id LEFT JOIN euroleague_team_names t2 ON h.team_id_b = t2.team_id WHERE game_id = %s", (game_id, ))
    team = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify({'team': team})

# Needed for populating Box Scores player dropdown
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
    cursor.execute("SELECT euroleague_team_names.team_id AS team_id, euroleague_team_names.team_name AS team_name, GROUP_CONCAT(euroleague_teams.season_code ORDER BY euroleague_teams.season_code ASC SEPARATOR ', ') AS seasons FROM euroleague_team_names LEFT JOIN euroleague_teams ON euroleague_team_names.team_id = euroleague_teams.team_id GROUP BY euroleague_team_names.team_id, euroleague_team_names.team_name")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_teams.html", team_names=team_names)

@admin_required
def panel_teams_add():
    team_id = request.form['team_id']
    team_name = request.form['team_name']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("INSERT INTO euroleague_team_names VALUES (%s, %s)", (team_id, team_name))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Team added successfully!", "success")
    return redirect(url_for('panel_teams_page'))

@admin_required
def panel_teams_update():
    old_team_id = request.form['old_team_id']
    team_id = request.form['team_id']
    team_name = request.form['team_name']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("UPDATE euroleague_team_names SET team_id = %s, team_name = %s WHERE team_id = %s", (team_id, team_name, old_team_id))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Team updated successfully!", "success")
    return redirect(url_for('panel_teams_page'))

@admin_required
def panel_teams_delete():
    team_id = request.form['team_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_team_names WHERE team_id = %s", (team_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Team deleted successfully!", "success")
    return redirect(url_for('panel_teams_page'))

@admin_required
def panel_team_seasons_page(team_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT *, euroleague_teams.team_id AS team_id, euroleague_team_names.team_name AS team_name FROM euroleague_teams LEFT JOIN euroleague_team_names ON euroleague_teams.team_id = euroleague_team_names.team_id WHERE euroleague_teams.team_id = %s", (team_id, ))
    team_seasons = cursor.fetchall()
    cursor.execute("SELECT COUNT(team_id) AS season_count FROM euroleague_teams WHERE team_id = %s", (team_id, ))
    season_count = cursor.fetchone()
    cursor.close()
    connection.close()

    for ts in team_seasons:
        ts['data_attributes'] = ' '.join([f'data-{key}={value}' for key, value in ts.items()])

    return render_template("panel_team_seasons.html", team_seasons=team_seasons, team_id=team_id, season_count=season_count)

@admin_required
def panel_team_seasons_add(team_id):
    form_data = request.form.to_dict()
    season_code = request.form['season_code']
    season_team_id = f"{season_code}_{team_id}"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_teams WHERE season_team_id = %s", (season_team_id, ))
    ts_existing = cursor.fetchone()
    if ts_existing:
        flash("This team season already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for("panel_team_seasons_page", team_id=team_id))
    
    cursor.execute("DESCRIBE euroleague_teams")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['season_team_id'] = season_team_id
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    sql = f"""INSERT INTO euroleague_teams ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Team season added successfully!", "success")
    return redirect(url_for("panel_team_seasons_page", team_id=team_id))

@admin_required
def panel_team_seasons_update(team_id):
    form_data = request.form.to_dict()
    season_code = request.form['season_code']
    season_team_id = request.form['season_team_id']
    new_season_team_id = f"{season_code}_{team_id}"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_teams WHERE season_team_id = %s", (new_season_team_id, ))
    ts_existing = cursor.fetchone()
    if ts_existing and season_team_id != new_season_team_id:
        flash("That season for this team already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for("panel_team_seasons_page", team_id=team_id))

    cursor.execute("DESCRIBE euroleague_teams")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['season_team_id'] = new_season_team_id
    filtered_data['old_season_team_id'] = season_team_id
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data if key != 'old_season_team_id'])
    sql = f"""UPDATE euroleague_teams SET {set_str} WHERE season_team_id = %(old_season_team_id)s"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Team season updated successfully!", "success")
    return redirect(url_for("panel_team_seasons_page", team_id=team_id))

@admin_required
def panel_team_seasons_delete(team_id):
    season_team_id = request.form['season_team_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_teams WHERE season_team_id = %s", (season_team_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Team season deleted successfully!", "success")
    return redirect(url_for("panel_team_seasons_page", team_id=team_id))

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
    filtered_data['game_player_id'] = new_game_player_id
    filtered_data['old_game_player_id'] = game_player_id
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data if key != 'old_game_player_id'])
    sql = f"""UPDATE euroleague_box_score SET {set_str} WHERE game_player_id = %(old_game_player_id)s"""
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

############################################################################################

@admin_required
def panel_matches_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT *, concat(score_a, ' - ', score_b) as result FROM euro.euroleague_header;")
    matches = cursor.fetchall()
    for match in matches:
        match['data_attributes'] = ' '.join([f'data-{key}={value}' for key, value in match.items()])
    cursor.close()
    connection.close()
    return render_template("panel_matches.html", matches=matches)

@admin_required
def panel_matches_add():
    form_data = request.form.to_dict()
    season_code = request.form['season_code']
    match_date = request.form['date']
    teamaid = request.form['team_id_a']
    teambid = request.form['team_id_b']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_header WHERE season_code = %s AND date = %s AND team_id_a = %s AND team_id_b = %s", (season_code, match_date, teamaid, teambid, ))
    ts_existing = cursor.fetchone()
    if ts_existing:
        flash("This game already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for("panel_matches_page"))
    
    cursor.execute("DESCRIBE euroleague_header")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    sql = f"""INSERT INTO euroleague_header ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Game added successfully!", "success")
    return redirect(url_for("panel_matches_page"))

@admin_required
def panel_matches_update():
    form_data = request.form.to_dict()

    for key, value in form_data.items():
        if value == "":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DESCRIBE euroleague_header")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data if key != 'game_id'])
    sql = f"""UPDATE euroleague_header SET {set_str} WHERE game_id = %(game_id)s"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Match updated successfully!", "success")
    return redirect(url_for("panel_matches_page"))

@admin_required
def panel_matches_delete():
    game_id = request.form['game_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_header WHERE game_id = %s", (game_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Match deleted successfully!", "success")
    return redirect(url_for("panel_matches_page"))