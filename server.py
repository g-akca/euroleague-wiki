from flask import Flask
import views, auth
from auth import refresh_session_data

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.secret_key = 'super secret key'

    app.add_url_rule("/", view_func=views.home_page)

    # Authentication related
    app.add_url_rule("/login", view_func=auth.login, methods=['GET', 'POST'])
    app.add_url_rule("/signup", view_func=auth.signup, methods=['GET', 'POST'])
    app.add_url_rule("/logout", view_func=auth.logout)
    app.add_url_rule("/update_account", view_func=auth.update_account, methods=['POST'])
    app.add_url_rule("/settings/get_teams", view_func=views.get_teams)

    # Category related
    app.add_url_rule("/teams", view_func=views.teams_page)
    app.add_url_rule("/team/<string:team_id>/<string:season_code>", view_func=views.team_details_page)
    app.add_url_rule("/team/<string:team_id>", view_func=views.team_details_page)
    app.add_url_rule("/players", view_func=views.players_page)
    app.add_url_rule("/matches", view_func=views.header_page)
    app.add_url_rule("/comparisons", view_func=views.comparisons_page)
    app.add_url_rule("/box_scores", view_func=views.box_scores_page)
    app.add_url_rule("/box_score/<string:box_score_id>", view_func=views.box_score_details_page)
    app.add_url_rule("/points", view_func=views.points_page)
    app.add_url_rule("/plays", view_func=views.play_by_play_page)

    # Admin Panel related
    app.add_url_rule("/panel", view_func=views.panel_users_page)
    app.add_url_rule("/panel/get_counts", view_func=views.get_counts)
    app.add_url_rule("/panel/users", view_func=views.panel_users_page)
    app.add_url_rule("/panel/teams", view_func=views.panel_teams_page)

    @app.before_request
    def refresh_before_request():
        refresh_session_data()

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
