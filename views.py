from flask import current_app, render_template
from server import get_db_connection

def home_page():
    return render_template("homepage.html")

def play_by_play_page():
    return render_template("play_by_play.html")

def player_names_page():
    players_ = current_app.config["players"]
    players = players_.get_players()
    return render_template("player_names.html", players=players)

def teams_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from euroleague_teams")
    teams = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("teams.html", teams=teams)