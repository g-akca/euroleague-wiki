from flask import Flask
import views, auth, panel

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
    app.add_url_rule("/settings/get_teams", view_func=auth.get_teams)
    app.add_url_rule("/403", view_func=auth.restricted)
    app.add_url_rule("/404", view_func=auth.not_found)

    # Category related
    app.add_url_rule("/teams", view_func=views.teams_page)
    app.add_url_rule("/team/<string:team_id>/<string:season_code>", view_func=views.team_details_page)
    app.add_url_rule("/team/<string:team_id>", view_func=views.team_details_page)
    app.add_url_rule("/players", view_func=views.players_page)
    app.add_url_rule("/player/<string:player_id>", view_func=views.player_details_page)
    app.add_url_rule("/player/<string:player_id>/<string:season_code>", view_func=views.player_details_page)
    app.add_url_rule("/matches", view_func=views.matches_page)
    app.add_url_rule("/match/<string:game_id>", view_func=views.match_details_page)
    app.add_url_rule("/seasons", view_func=views.seasons_page)
    app.add_url_rule("/season/<string:season_code>", view_func=views.season_details_page)

    # Admin Panel related
    app.add_url_rule("/panel", view_func=panel.panel_users_page)
    app.add_url_rule("/panel/get_counts", view_func=panel.get_counts)
    app.add_url_rule("/panel/get_teams_by_match/<string:game_id>", view_func=panel.get_teams_by_match)
    app.add_url_rule("/panel/get_players_by_team_season/<string:team_id>/<string:season_code>", view_func=panel.get_players_by_team_season)
    app.add_url_rule("/panel/users", view_func=panel.panel_users_page)
    app.add_url_rule("/panel/users/add", view_func=panel.panel_users_add, methods=['POST'])
    app.add_url_rule("/panel/users/update", view_func=panel.panel_users_update, methods=['POST'])
    app.add_url_rule("/panel/users/delete", view_func=panel.panel_users_delete, methods=['POST'])
    app.add_url_rule("/panel/teams", view_func=panel.panel_teams_page)
    app.add_url_rule("/panel/teams/add", view_func=panel.panel_teams_add, methods=['POST'])
    app.add_url_rule("/panel/teams/update", view_func=panel.panel_teams_update, methods=['POST'])
    app.add_url_rule("/panel/teams/delete", view_func=panel.panel_teams_delete, methods=['POST'])
    app.add_url_rule("/panel/teams/<string:team_id>", view_func=panel.panel_team_seasons_page)
    app.add_url_rule("/panel/teams/<string:team_id>/add", view_func=panel.panel_team_seasons_add, methods=['POST'])
    app.add_url_rule("/panel/teams/<string:team_id>/update", view_func=panel.panel_team_seasons_update, methods=['POST'])
    app.add_url_rule("/panel/teams/<string:team_id>/delete", view_func=panel.panel_team_seasons_delete, methods=['POST'])
    app.add_url_rule("/panel/box_scores", view_func=panel.panel_box_scores_page)
    app.add_url_rule("/panel/box_scores/add", view_func=panel.panel_box_scores_add, methods=['POST'])
    app.add_url_rule("/panel/box_scores/update", view_func=panel.panel_box_scores_update, methods=['POST'])
    app.add_url_rule("/panel/box_scores/delete", view_func=panel.panel_box_scores_delete, methods=['POST'])
    app.add_url_rule("/panel/matches", view_func=panel.panel_matches_page)
    app.add_url_rule("/panel/matches/add", view_func=panel.panel_matches_add, methods=['POST'])
    app.add_url_rule("/panel/matches/update", view_func=panel.panel_matches_update, methods=['POST'])
    app.add_url_rule("/panel/matches/delete", view_func=panel.panel_matches_delete, methods=['POST'])
    app.add_url_rule("/panel/plays", view_func=panel.panel_plays_page)
    app.add_url_rule("/panel/plays/add", view_func=panel.panel_plays_add, methods=['POST'])
    app.add_url_rule("/panel/plays/update", view_func=panel.panel_plays_update, methods=['POST'])
    app.add_url_rule("/panel/plays/delete", view_func=panel.panel_plays_delete, methods=['POST'])
    app.add_url_rule("/panel/players", view_func=panel.panel_players_page)
    app.add_url_rule("/panel/players/add", view_func=panel.panel_players_add, methods=['POST'])
    app.add_url_rule("/panel/players/update", view_func=panel.panel_players_update, methods=['POST'])
    app.add_url_rule("/panel/players/delete", view_func=panel.panel_players_delete, methods=['POST'])
    app.add_url_rule("/panel/players/<string:player_id>", view_func=panel.panel_player_seasons_page)
    app.add_url_rule("/panel/players/<string:player_id>/add", view_func=panel.panel_player_seasons_add, methods=['POST'])
    app.add_url_rule("/panel/players/<string:player_id>/update", view_func=panel.panel_player_seasons_update, methods=['POST'])
    app.add_url_rule("/panel/players/<string:player_id>/delete", view_func=panel.panel_player_seasons_delete, methods=['POST'])

    @app.before_request
    def refresh_before_request():
        auth.refresh_session_data()
    
    @app.errorhandler(403)
    def page_restricted(e):
        return auth.restricted()

    @app.errorhandler(404)
    def page_not_found(e):
        return auth.not_found()

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
