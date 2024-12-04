from flask import Flask
from player import *
import views, auth

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.secret_key = 'super secret key'

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=auth.login, methods=['GET', 'POST'])
    app.add_url_rule("/signup", view_func=auth.signup, methods=['GET', 'POST'])
    app.add_url_rule("/logout", view_func=auth.logout)
    app.add_url_rule("/update_account", view_func=auth.update_account, methods=['POST'])
    app.add_url_rule("/play_by_play", view_func=views.play_by_play_page)
    app.add_url_rule("/player_names", view_func=views.player_names_page)
    app.add_url_rule("/teams", view_func=views.teams_page)
    app.add_url_rule("/team/<string:team_id>/<string:season_code>", view_func=views.team_details_page)
    app.add_url_rule("/team/<string:team_id>", view_func=views.team_details_page)
    app.add_url_rule("/comparison", view_func=views.comparison_page)
    app.add_url_rule("/header", view_func=views.header_page)
    app.add_url_rule("/box_scores", view_func=views.box_scores_page)
    app.add_url_rule("/box_score/<string:box_score_id>", view_func=views.box_score_details_page)
    app.add_url_rule("/players", view_func=views.players_page)
    app.add_url_rule("/points", view_func=views.points_page)

    players = PlayerCollection()
    
    app.config["players"] = players

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
