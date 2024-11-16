from flask import current_app, render_template

def home_page():
    return render_template("homepage.html")

def play_by_play_page():
    return render_template("play_by_play.html")

def player_names_page():
    players_ = current_app.config["players"]
    players = players_.get_players()
    return render_template("player_names.html", players=players)
