from flask import current_app, render_template, request
from server import get_db_connection

def home_page():
    return render_template("homepage.html")

def play_by_play_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_play_by_play")
    pbp = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("play_by_play.html", pbp=pbp)

def player_names_page():
    connection = get_db_connection()
    sort_by = request.args.get('sort_by', 'player_id asc')
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query_returner(sort_by, "euroleague_player_names"))
    player_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("player_names.html", player_names=player_names, sort_by=sort_by)

def query_returner(x, y):
    return (f"select * from {y} order by {x}")

def teams_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_teams")
    teams = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("teams.html", teams=teams)

def header_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_header")
    header = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("header.html", header=header)

def comparison_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_comparison")
    comparison = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("comparison.html", comparison=comparison)

def box_score_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_box_score")
    box_score = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("box_score.html", box_score=box_score)

def players_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_players")
    players = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("players.html", players=players)

def points_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_points")
    points = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("points.html", points=points)