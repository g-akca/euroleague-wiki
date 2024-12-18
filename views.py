from flask import render_template, request, flash
from db import get_db_connection
from mysql.connector import Error
import queries

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
    sort_by = request.args.get('sort_by', 'player_id asc') #default sort'u ayarlayabiliyoruz
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').strip()
    page_button = 4
    
    if search_query:
        where = f"WHERE player_name LIKE \"%{search_query}%\""
    else:
        where = ""

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
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
        end_page = min(page_num + page_button, page_count)
    )

def player_details_page(player_id, season_code=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_player_names WHERE player_id = %s", (player_id, ))
    player_name = cursor.fetchone()
    cursor.execute("SELECT * FROM euroleague_players WHERE player_id = %s", (player_id, ))
    player_seasons = cursor.fetchall()

    if season_code:
        cursor.execute("SELECT * FROM euroleague_players WHERE player_id = %s AND season_code = %s", (player_id, season_code))
        season_data = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM euroleague_players WHERE player_id = %s AND season_code = (SELECT MAX(season_code) FROM euroleague_players WHERE player_id = %s)", (player_id, player_id))
        season_data = cursor.fetchone()

    cursor.close()
    connection.close()
    return render_template("player_details.html", player_name=player_name, player_seasons=player_seasons, season_data=season_data)

def query_returner_per_page(x, y, z, u, s):
    return f"SELECT * FROM {y} {s} ORDER BY {x} LIMIT {z} OFFSET {u};"

def teams_page():
    sort_by = request.args.get('sort_by', 'team_id asc')
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').strip()
    page_button = 4
    
    if search_query:
        where = f"WHERE team_name LIKE \"%{search_query}%\""
    else:
        where = ""

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_team_names")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute(query_returner_per_page(sort_by, "euroleague_team_names", page_limit, (page_num-1) * page_limit, where))
    team_names = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template(
        "teams.html", 
        team_names=team_names, 
        sort_by=sort_by, 
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count)
    )

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

def matches_page():
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    page_button = 4
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_header")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1)
    cursor.execute("SELECT h.*, t1.team_name AS team_a, t2.team_name AS team_b FROM euroleague_header h LEFT JOIN euroleague_team_names t1 ON h.team_id_a = t1.team_id LEFT JOIN euroleague_team_names t2 ON h.team_id_b = t2.team_id ORDER BY date, time ASC LIMIT %s OFFSET %s", (page_limit, (page_num-1) * page_limit))
    matches = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template(
        "matches.html", 
        matches=matches,
        page_num=page_num,
        page_count=page_count,
        end_page = min(page_num + page_button, page_count)
    )

def match_details_page(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT h.*, t1.team_name AS team_a, t2.team_name AS team_b FROM euroleague_header h LEFT JOIN euroleague_team_names t1 ON h.team_id_a = t1.team_id LEFT JOIN euroleague_team_names t2 ON h.team_id_b = t2.team_id WHERE game_id = %s", (game_id, ))
    match = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template("match_details.html", match=match)

def seasons_page():
    return render_template("seasons.html")

def box_scores_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT t1.game AS game_id, t1.team_id AS team_1_id, t1.points AS player_1_points, t2.points AS player_2_points, t2.team_id AS team_2_id FROM (SELECT a.game_id AS game, a.player_id AS player_id, a.team_id AS team_id, a.points AS points FROM euroleague_box_score a LEFT JOIN euroleague_player_names b ON a.player_id = b.player_id LEFT JOIN euroleague_team_names c ON a.team_id = c.team_id WHERE a.player_id = a.team_id) t1 JOIN (SELECT a.game_id AS game, a.player_id AS player_id, a.team_id AS team_id, a.points AS points FROM euroleague_box_score a LEFT JOIN euroleague_player_names b ON a.player_id = b.player_id LEFT JOIN euroleague_team_names c ON a.team_id = c.team_id WHERE a.player_id = a.team_id) t2 ON t1.game = t2.game AND t1.team_id < t2.team_id LIMIT 100;")
    box_scores = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("box_scores.html", box_scores=box_scores)

def box_score_details_page(game_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_box_score a LEFT JOIN euroleague_player_names b ON a.player_id = b.player_id LEFT JOIN euroleague_team_names c ON a.team_id = c.team_id WHERE a.player_id != a.team_id AND game_id = %s ORDER BY team_name, minutes DESC;", (game_id,))
    box_score = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("box_score_details.html", box_score=box_score)
