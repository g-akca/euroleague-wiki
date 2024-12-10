from flask import render_template, request, jsonify, flash
from db import get_db_connection
from mysql.connector import Error
import queries

def get_teams():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names ORDER BY team_name ASC")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(team_names)

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

def home_page():
    return render_template("homepage.html")

def play_by_play_page():
    connection = get_db_connection()
    if connection is None:
        flash("Couldn't connect to the database.", "danger")
        return render_template("play_by_play.html", data=[])
    try: 
        cursor = connection.cursor(dictionary=True)
        query = queries.play_by_play_query
        cursor.execute(query)
        data = cursor.fetchall()

    except Error as e: 
        flash(f"Query failed: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template("play_by_play.html", data=data)

def players_page():
    connection = get_db_connection()
    sort_by = request.args.get('sort_by', 'player_id asc') #default sort'u ayarlayabiliyoruz
    page_limit = 30
    page_num = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').strip()
    page_button = 5
    
    cursor = connection.cursor(dictionary=True)
    
    if search_query:
        where = f"WHERE player_name LIKE \"%{search_query}%\""
    else:
        where = ""

    cursor.execute("SELECT COUNT(*) as total FROM euroleague_player_names")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute(query_returner_per_page(sort_by, "euroleague_player_names", page_limit, (page_num-1) * page_limit, where))
    player_names = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template(
        "players.html", 
        player_names=player_names, 
        sort_by=sort_by, 
        page_num=page_num,
        page_count=page_count,
        page_button=page_button,
        end_page = min(page_num + page_button - 1, page_count)
    )

def query_returner_per_page(x, y, z, u, s):
    return f"SELECT * FROM {y} {s} ORDER BY {x} LIMIT {z} OFFSET {u};"

def teams_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("teams.html", team_names=team_names)

def team_details_page(team_id, season_code=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names WHERE team_id = %s", (team_id, ))
    team_name = cursor.fetchone()
    cursor.execute("SELECT * FROM euroleague_teams WHERE team_id = %s", (team_id, ))
    team_seasons = cursor.fetchall()

    if season_code:
        cursor.execute("SELECT * FROM euroleague_teams WHERE team_id = %s AND season_code = %s", (team_id, season_code))
        season_data = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM euroleague_teams WHERE team_id = %s AND season_code = (SELECT MAX(season_code) FROM euroleague_teams WHERE team_id = %s)", (team_id, team_id))
        season_data = cursor.fetchone()

    cursor.close()
    connection.close()
    return render_template("team_details.html", team_name=team_name, team_seasons=team_seasons, season_data=season_data)

def header_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_header")
    header = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("header.html", header=header)

def comparisons_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_comparison")
    comparisons = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("comparisons.html", comparisons=comparisons)

def box_scores_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_box_score")
    box_scores = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("box_scores.html", box_scores=box_scores)

def box_score_details_page(box_score_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_box_score WHERE game_player_id = %s", (box_score_id, ))
    box_score = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template("box_score_details.html", box_score=box_score)

def points_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_points")
    points = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("points.html", points=points)

def panel_users_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT *, CASE WHEN role = 'U' THEN 'User' WHEN role = 'A' THEN 'Admin' ELSE 'Unknown' END AS role_detailed FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_users.html", users=users)

def panel_teams_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_team_names")
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("panel_teams.html", team_names=team_names)
