from flask import Flask
from player import *
import views

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/play_by_play", view_func=views.play_by_play_page)
    app.add_url_rule("/player_names", view_func=views.player_names_page)

    players = PlayerCollection()
    players.add_player(Player("P001", "Bogdan Bogdanovic"))
    players.add_player(Player("P002", "Vasilije Micic"))
    players.add_player(Player("P003", "Shane Larkin"))
    players.add_player(Player("P004", "Nikola Mirotic"))
    players.add_player(Player("P005", "Mike James"))
    
    app.config["players"] = players

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
