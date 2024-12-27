from flask import render_template, request, jsonify, flash, redirect, url_for, session
from db import get_db_connection
from auth import admin_required
import bcrypt
import urllib.parse

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

# Needed for dynamically populating Box Scores and Plays team dropdown
@admin_required
def get_teams_by_match(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT t1.team_name AS team_a, t2.team_name AS team_b, team_id_a, team_id_b FROM euroleague_header h LEFT JOIN euroleague_team_names t1 ON h.team_id_a = t1.team_id LEFT JOIN euroleague_team_names t2 ON h.team_id_b = t2.team_id WHERE game_id = %s", (game_id, ))
    team = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify({'team': team})

# Needed for dynamically populating Box Scores and Plays player dropdown
@admin_required
def get_players_by_team_season(team_id, season_code):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT euroleague_player_names.player_id, euroleague_player_names.player_name FROM euroleague_players LEFT JOIN euroleague_player_names ON euroleague_players.player_id = euroleague_player_names.player_id WHERE team_id = %s AND season_code = %s ORDER BY euroleague_player_names.player_name ASC", (team_id, season_code))
    players = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'players': players})

# Users Panel
@admin_required
def panel_users_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM users")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT *, CASE WHEN role = 'U' THEN 'User' WHEN role = 'A' THEN 'Admin' ELSE 'Unknown' END AS role_detailed FROM users LEFT JOIN euroleague_team_names ON users.team_supported = euroleague_team_names.team_id LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit ))
    users = cursor.fetchall()

    for user in users:
        user['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in user.items()])

    cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_users.html", 
        users=users, 
        team_names=team_names, 
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

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
    user_id = int(request.form['user_id'])
    own_id = session['user_id']

    if user_id == own_id:
        flash("You can't delete your own account!", "danger")
        return redirect(url_for("panel_users_page"))
    else:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id, ))
        connection.commit()
        cursor.close()
        connection.close()

        flash("User deleted successfully!", "success")
        return redirect(url_for('panel_users_page'))

# Teams Panel
@admin_required
def panel_teams_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_team_names")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT euroleague_team_names.team_id AS team_id, euroleague_team_names.team_name AS team_name, GROUP_CONCAT(euroleague_teams.season_code ORDER BY euroleague_teams.season_code ASC SEPARATOR ', ') AS seasons FROM euroleague_team_names LEFT JOIN euroleague_teams ON euroleague_team_names.team_id = euroleague_teams.team_id GROUP BY euroleague_team_names.team_id, euroleague_team_names.team_name LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit ))
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_teams.html", 
        team_names=team_names,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

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

# Team Seasons Panel
@admin_required
def panel_team_seasons_page(team_id):
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(team_id) AS season_count FROM euroleague_teams WHERE team_id = %s", (team_id, ))
    season_count = cursor.fetchone()
    page_count = (season_count['season_count'] + page_limit - 1) // page_limit
    cursor.execute("SELECT *, euroleague_teams.team_id AS team_id, euroleague_team_names.team_name AS team_name FROM euroleague_teams LEFT JOIN euroleague_team_names ON euroleague_teams.team_id = euroleague_team_names.team_id WHERE euroleague_teams.team_id = %s LIMIT %s OFFSET %s", (team_id, page_limit, (page_num-1) * page_limit ))
    team_seasons = cursor.fetchall()

    for ts in team_seasons:
        ts['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in ts.items()])

    cursor.close()
    connection.close()

    return render_template("panel_team_seasons.html", 
        team_seasons=team_seasons, 
        team_id=team_id, 
        season_count=season_count,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

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

# Box Scores Panel
@admin_required
def panel_box_scores_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_box_score")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT *, euroleague_box_score.player_id AS player_id, euroleague_box_score.team_id AS team_id FROM euroleague_box_score LEFT JOIN euroleague_player_names ON euroleague_box_score.player_id = euroleague_player_names.player_id LEFT JOIN euroleague_team_names ON euroleague_box_score.team_id = euroleague_team_names.team_id ORDER BY game_id ASC, euroleague_box_score.team_id ASC, points DESC LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit ))
    box_scores = cursor.fetchall()

    for bx in box_scores:
        bx['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in bx.items()])

    cursor.execute("SELECT * FROM euroleague_header")
    matches = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_box_scores.html", 
        box_scores=box_scores,
        matches=matches,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

@admin_required
def panel_box_scores_add():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']
    player_id = request.form['player_id']
    game_player_id = f"{game_id}_{player_id}"

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

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

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

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

# Matches Panel
@admin_required
def panel_matches_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_header")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT *, concat(score_a, ' - ', score_b) as result FROM euro.euroleague_header LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit))
    matches = cursor.fetchall()

    for match in matches:
        match['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in match.items()])

    cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
    teams = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_matches.html", 
        matches=matches,
        teams=teams,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

@admin_required
def panel_matches_add():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']
    team_a = request.form['team_id_a']
    team_b = request.form['team_id_b']
    game = f"{team_a}-{team_b}"

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_header WHERE game_id = %s", (game_id, ))
    match_existing = cursor.fetchone()
    if match_existing:
        flash("This match already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for("panel_matches_page"))
    
    cursor.execute("DESCRIBE euroleague_header")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game'] = game
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    sql = f"""INSERT INTO euroleague_header ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Match added successfully!", "success")
    return redirect(url_for("panel_matches_page"))

@admin_required
def panel_matches_update():
    form_data = request.form.to_dict()
    team_a = request.form['team_id_a']
    team_b = request.form['team_id_b']
    game = f"{team_a}-{team_b}"

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DESCRIBE euroleague_header")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game'] = game
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

# Plays Panel
@admin_required
def panel_plays_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_play_by_play")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT *, play.player_id AS player_id, play.team_id AS team_id, CASE WHEN play.quarter = 'q1' THEN 'Quarter 1' WHEN play.quarter = 'q2' THEN 'Quarter 2' WHEN play.quarter = 'q3' THEN 'Quarter 3' WHEN play.quarter = 'q4' THEN 'Quarter 4' WHEN play.quarter = 'extra_time' THEN 'Overtime' ELSE 'Unknown' END AS quarter_description FROM euroleague_play_by_play as play LEFT JOIN euroleague_player_names ON play.player_id = euroleague_player_names.player_id LEFT JOIN euroleague_team_names ON play.team_id = euroleague_team_names.team_id ORDER BY game_id, number_of_play ASC LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit))
    plays = cursor.fetchall()

    for play in plays:
        play['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in play.items()])

    cursor.execute("SELECT * FROM euroleague_header")
    matches = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_plays.html", 
        plays=plays, 
        matches=matches,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

@admin_required
def panel_plays_add():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']
    play_num = int(request.form['number_of_play'])

    if play_num < 0:
        flash("Number of play cannot be below 0!")
        return redirect(url_for('panel_plays_page'))
    elif play_num < 10:
        game_play_id = f"{game_id}_00{play_num}"
    elif play_num < 100:
        game_play_id = f"{game_id}_0{play_num}"
    else:
        game_play_id = f"{game_id}_{play_num}"

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_play_by_play WHERE game_play_id = %s", (game_play_id, ))
    play_existing = cursor.fetchone()
    if play_existing:
        flash("The number of play given already exists in the match!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for('panel_plays_page'))
    
    cursor.execute("DESCRIBE euroleague_play_by_play")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game_play_id'] = game_play_id
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    sql = f"""INSERT INTO euroleague_play_by_play ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Play added successfully!", "success")
    return redirect(url_for('panel_plays_page'))

@admin_required
def panel_plays_update():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']
    play_num = int(request.form['number_of_play'])
    game_play_id = request.form['game_play_id']

    if play_num < 0:
        flash("Number of play cannot be below 0!")
        return redirect(url_for('panel_plays_page'))
    elif play_num < 10:
        new_game_play_id = f"{game_id}_00{play_num}"
    elif play_num < 100:
        new_game_play_id = f"{game_id}_0{play_num}"
    else:
        new_game_play_id = f"{game_id}_{play_num}"

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_play_by_play WHERE game_play_id = %s", (new_game_play_id, ))
    play_existing = cursor.fetchone()
    if play_existing and game_play_id != new_game_play_id:
        flash("The number of play given already exists in that match!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for('panel_plays_page'))

    cursor.execute("DESCRIBE euroleague_play_by_play")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game_play_id'] = new_game_play_id
    filtered_data['old_game_play_id'] = game_play_id
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data if key != 'old_game_play_id'])
    sql = f"""UPDATE euroleague_play_by_play SET {set_str} WHERE game_play_id = %(old_game_play_id)s"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Play updated successfully!", "success")
    return redirect(url_for('panel_plays_page'))

@admin_required
def panel_plays_delete():
    game_play_id = request.form['game_play_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_play_by_play WHERE game_play_id = %s", (game_play_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Play deleted successfully!", "success")
    return redirect(url_for('panel_plays_page'))

#Comparisons Panel
@admin_required
def panel_comparisons_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_comparison")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("""
        SELECT C.*, H.*,
        T1.team_name AS team_name_a,
        T2.team_name AS team_name_b
        FROM euroleague_comparison AS C
        LEFT JOIN euroleague_header AS H ON C.game_id = H.game_id
        LEFT JOIN euroleague_team_names T1 ON H.team_id_a = T1.team_id
        LEFT JOIN euroleague_team_names T2 ON H.team_id_b = T2.team_id
        ORDER BY H.game_id
        LIMIT %s OFFSET %s;
    """,(page_limit, (page_num-1) * page_limit ))
    comparisons = cursor.fetchall()

    for comp in comparisons:
        comp['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in comp.items()])

    cursor.execute("""
        SELECT H.game_id,
        T1.team_name AS team_name_a,
        T2.team_name AS team_name_b   
        FROM euroleague_header H
        LEFT JOIN euroleague_team_names T1 ON H.team_id_a = T1.team_id
        LEFT JOIN euroleague_team_names T2 ON H.team_id_b = T2.team_id
    """)
    matches= cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_comparisons.html", 
        comparisons=comparisons,
        matches=matches, 
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

@admin_required
def get_playing_teams(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            T1.team_name AS team_name_a,
            T2.team_name AS team_name_b
        FROM euroleague_header H
        LEFT JOIN euroleague_team_names T1 ON H.team_id_a = T1.team_id
        LEFT JOIN euroleague_team_names T2 ON H.team_id_b = T2.team_id
        WHERE H.game_id = %s
    """, (game_id,))
    
    team_data = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if team_data:
        return jsonify(team_data)
    else:
        return jsonify({"team_name_a": None, "team_name_b": None})

@admin_required
def panel_comparisons_add():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM euroleague_comparison WHERE game_id = %s", (game_id,))
    comparison_existing = cursor.fetchone()
    if comparison_existing:
        flash("This comparison already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for('panel_comparisons_page'))
    
    cursor.execute("DESCRIBE euroleague_comparison")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['game_id'] = game_id
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    #TO:DO Some of the varchar columns are missing
    sql = f"""INSERT INTO euroleague_comparison ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    connection.close()
    cursor.close()

    flash("Comparison added successfully!", "success")
    return redirect(url_for('panel_comparisons_page'))

@admin_required
def panel_comparisons_update():
    form_data = request.form.to_dict()
    game_id = request.form['game_id']

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_comparison WHERE game_id = %s", (game_id,))
    original_data = cursor.fetchone()

    if not original_data:
        flash('Comparison record not found.', 'danger')
        return redirect(url_for('panel_comparisons_page'))
    
    has_changed = any(str(original_data[key]) != form_data[key] for key in original_data if key in form_data)
    if not has_changed:
        flash('No changes were made. Update canceled.', 'warning')
        return redirect(url_for('panel_comparisons_page'))

    cursor.execute("DESCRIBE euroleague_comparison")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data])
    sql = f"""UPDATE euroleague_comparison SET {set_str} WHERE game_id = %(game_id)s"""

    cursor.execute(sql, filtered_data)
    connection.commit()

    cursor.close()
    connection.close()

    flash("Comparison updated successfully!", "success")
    return redirect(url_for('panel_comparisons_page'))

@admin_required
def panel_comparisons_delete():
    game_id = request.form['game_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_comparison WHERE game_id = %s", (game_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Comparison deleted successfully!", "success")
    return redirect(url_for('panel_comparisons_page'))

@admin_required
def panel_players_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_player_names")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT euroleague_player_names.player_id AS player_id, euroleague_player_names.player_name AS player_name, GROUP_CONCAT(euroleague_players.season_code ORDER BY euroleague_players.season_code ASC SEPARATOR ', ') AS seasons FROM euroleague_player_names LEFT JOIN euroleague_players ON euroleague_player_names.player_id = euroleague_players.player_id GROUP BY euroleague_player_names.player_id, euroleague_player_names.player_name LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit ))
    player_names = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_players.html", 
        player_names=player_names,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

@admin_required
def panel_players_add():
    player_id = request.form['player_id']
    player_name = request.form['player_name']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("INSERT INTO euroleague_player_names VALUES (%s, %s)", (player_id, player_name))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Player added successfully!", "success")
    return redirect(url_for('panel_players_page'))

@admin_required
def panel_players_update():
    old_player_id = request.form['old_player_id']
    player_id = request.form['player_id']
    player_name = request.form['player_name']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("UPDATE euroleague_player_names SET player_id = %s, player_name = %s WHERE player_id = %s", (player_id, player_name, old_player_id))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Player updated successfully!", "success")
    return redirect(url_for('panel_players_page'))

@admin_required
def panel_players_delete():
    player_id = request.form['player_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_player_names WHERE player_id = %s", (player_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Player deleted successfully!", "success")
    return redirect(url_for('panel_players_page'))

@admin_required
def panel_player_seasons_page(player_id):
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
    teams = cursor.fetchall()
    cursor.execute("SELECT COUNT(player_id) AS season_count FROM euroleague_players WHERE player_id = %s", (player_id, ))
    season_count = cursor.fetchone()
    page_count = (season_count['season_count'] + page_limit - 1) // page_limit
    cursor.execute("SELECT *, euroleague_players.player_id AS player_id, euroleague_player_names.player_name AS player_name FROM euroleague_players LEFT JOIN euroleague_player_names ON euroleague_players.player_id = euroleague_player_names.player_id WHERE euroleague_players.player_id = %s LIMIT %s OFFSET %s", (player_id, page_limit, (page_num-1) * page_limit ))
    player_seasons = cursor.fetchall()

    for ts in player_seasons:
        ts['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in ts.items()])

    cursor.close()
    connection.close()

    return render_template("panel_player_seasons.html", 
        player_seasons=player_seasons, 
        player_id=player_id, 
        season_count=season_count,
        teams=teams,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))

@admin_required
def panel_player_seasons_add(player_id):
    form_data = request.form.to_dict()
    season_code = request.form['season_code']
    season_player_id = f"{season_code}_{player_id}"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_players WHERE season_player_id = %s", (season_player_id, ))
    ts_existing = cursor.fetchone()
    if ts_existing:
        flash("This player season already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for("panel_player_seasons_page", player_id=player_id))
    
    cursor.execute("DESCRIBE euroleague_players")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['season_player_id'] = season_player_id
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    sql = f"""INSERT INTO euroleague_players ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Player season added successfully!", "success")
    return redirect(url_for("panel_player_seasons_page", player_id=player_id))

@admin_required
def panel_player_seasons_update(player_id):
    form_data = request.form.to_dict()
    season_code = request.form['season_code']
    season_player_id = request.form['season_player_id']
    new_season_player_id = f"{season_code}_{player_id}"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_players WHERE season_player_id = %s", (new_season_player_id, ))
    ts_existing = cursor.fetchone()
    if ts_existing and season_player_id != new_season_player_id:
        flash("That season for this player already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for("panel_player_seasons_page", player_id=player_id))

    cursor.execute("DESCRIBE euroleague_players")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    filtered_data['season_player_id'] = new_season_player_id
    filtered_data['old_season_player_id'] = season_player_id
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data if key != 'old_season_player_id'])
    sql = f"""UPDATE euroleague_players SET {set_str} WHERE season_player_id = %(old_season_player_id)s"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Player season updated successfully!", "success")
    return redirect(url_for("panel_player_seasons_page", player_id=player_id))

@admin_required
def panel_player_seasons_delete(player_id):
    season_player_id = request.form['season_player_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_players WHERE season_player_id = %s", (season_player_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Player season deleted successfully!", "success")
    return redirect(url_for("panel_player_seasons_page", player_id=player_id))

#Points Panel
@admin_required
def panel_points_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_points")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("""
        SELECT *
        FROM euroleague_points AS points
        LEFT JOIN euroleague_play_by_play AS plays ON points.game_play_id = plays.game_play_id
        LEFT JOIN euroleague_player_names AS player_names ON plays.player_id = player_names.player_id
        ORDER BY points.primary_point_id   
        LIMIT %s OFFSET %s;
    """,(page_limit, (page_num-1) * page_limit ))
    points = cursor.fetchall()

    for point in points:
        point['data_attributes'] = ' '.join([f'data-{key}={urllib.parse.quote(str(value))}' for key, value in point.items()])

    cursor.execute("""
        SELECT game_id
        FROM euroleague_header
    """)
    games = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("panel_points.html", 
        points=points,
        games=games, 
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count))


@admin_required
def get_plays_by_game(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT game_id, game_play_id
        FROM euroleague_play_by_play
        WHERE game_id = %s
    """, (game_id,))
    
    plays_data = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify({"game_plays": plays_data or []})


@admin_required
def panel_points_add():
    form_data = request.form.to_dict()
    game_play_id = request.form['game_play_id']
    action = form_data.get('action')

    points_map = {
        "Missed Two Pointer": '0',
        "Two Pointer": '2',
        "Missed Three Pointer": '0',
        "Three Pointer": '3',
        "Free Throw In": '1',
        "Missed Layup": '0',
        "Layup Made": '2',
        "Dunk": '2',
    }

    form_data['points'] = points_map.get(action, 0)

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM euroleague_points WHERE game_play_id = %s", (game_play_id,))
    points_existing = cursor.fetchone()
    if points_existing:
        flash("This point already exists!", "danger")
        cursor.close()
        connection.close()
        return redirect(url_for('panel_points_page'))
    
    cursor.execute("DESCRIBE euroleague_points")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    
    value_placeholders = ', '.join([f'%({key})s' for key in filtered_data])
    columns_str = ', '.join(filtered_data.keys())
    
    sql = f"""INSERT INTO euroleague_points ({columns_str}) VALUES ({value_placeholders})"""
    cursor.execute(sql, filtered_data)
    connection.commit()
    connection.close()
    cursor.close()

    flash("Points added successfully!", "success")
    return redirect(url_for('panel_points_page'))

@admin_required
def panel_points_update():
    form_data = request.form.to_dict()
    game_play_id = request.form['game_play_id']
    action = form_data.get('action')

    points_map = {
        "Missed Two Pointer": '0',
        "Two Pointer": '2',
        "Missed Three Pointer": '0',
        "Three Pointer": '3',
        "Free Throw In": '1',
        "Missed Layup": '0',
        "Layup Made": '2',
        "Dunk": '2',
    }

    form_data['points'] = points_map.get(action, 0)

    for key, value in form_data.items():
        if value == "" or value == "None":
            form_data[key] = None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_points WHERE game_play_id = %s", (game_play_id,))
    original_data = cursor.fetchone()

    if not original_data:
        flash('Point record not found.', 'danger')
        return redirect(url_for('panel_points_page'))
    
    has_changed = any(str(original_data[key]) != form_data[key] for key in original_data if key in form_data)
    if not has_changed:
        flash('No changes were made. Update canceled.', 'warning')
        return redirect(url_for('panel_points_page'))

    form_data['fastbreak'] = form_data.get('fastbreak', None)
    form_data['second_chance'] = form_data.get('second_chance', None)
    form_data['points_off_turnover'] = form_data.get('points_off_turnover', None)

    cursor.execute("DESCRIBE euroleague_points")
    columns = [column['Field'] for column in cursor.fetchall()]
    filtered_data = {key: form_data[key] for key in form_data if key in columns}
    
    set_str = ', '.join([f"{key} = %({key})s" for key in filtered_data])
    sql = f"""UPDATE euroleague_points SET {set_str} WHERE game_play_id = %(game_play_id)s"""

    cursor.execute(sql, filtered_data)
    connection.commit()
    cursor.close()
    connection.close()

    flash("Point updated successfully!", "success")
    return redirect(url_for('panel_points_page'))

@admin_required
def panel_points_delete():
    game_play_id = request.form['game_play_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM euroleague_points WHERE game_play_id = %s", (game_play_id, ))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Point deleted successfully!", "success")
    return redirect(url_for('panel_points_page'))
    

   
