from flask import current_app, render_template, request
from db import get_db_connection

def home_page():
    return render_template("homepage.html")

def play_by_play_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_play_by_play")
    pbp = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("play_by_play.html", pbp=pbp)

def player_names_page():
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
        "player_names.html", 
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

def comparison_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_comparison")
    comparison = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("comparison.html", comparison=comparison)

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

def players_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_players")
    players = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("players.html", players=players)

def points_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM euroleague_points")
    points = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("points.html", points=points)
