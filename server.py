from flask import Flask
from player import *
import views, mysql.connector

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.secret_key = 'super secret key'

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login, methods=['GET', 'POST'])
    app.add_url_rule("/signup", view_func=views.signup, methods=['GET', 'POST'])
    app.add_url_rule("/logout", view_func=views.logout)
    app.add_url_rule("/play_by_play", view_func=views.play_by_play_page)
    app.add_url_rule("/player_names", view_func=views.player_names_page)
    app.add_url_rule("/teams", view_func=views.teams_page)
    app.add_url_rule("/comparison", view_func=views.comparison_page)
    app.add_url_rule("/header", view_func=views.header_page)
    app.add_url_rule("/box_score", view_func=views.box_score_page)
    app.add_url_rule("/players", view_func=views.players_page)
    app.add_url_rule("/points", view_func=views.points_page)

    players = PlayerCollection()
    
    app.config["players"] = players

    return app

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="euro"
    )
    return connection


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
