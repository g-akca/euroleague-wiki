from flask import render_template, request
from db import get_db_connection
import random

def home_page():
    return render_template("homepage.html")

def players_page():
    sort_by = request.args.get('sort_by', 'player_id asc')  
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').strip()
    page_button = 4
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM euroleague_player_names")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit

    if page_num < 1:
        page_num = 1
    elif page_num > page_count:
        page_num = page_count

    if search_query:
        where = f"WHERE player_name LIKE \"%{search_query}%\""
        page_limit = 100
    else:
        where = ""

    cursor.execute(query_returner_per_page(sort_by, "euroleague_player_names", page_limit, (page_num - 1) * page_limit, where))
    player_names = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "players.html",
        player_names=player_names,
        sort_by=sort_by,
        page_num=page_num,
        page_count=page_count,
        end_page=min(page_num + page_button, page_count)
    )


def query_returner_per_page(x, y, z, u, s):
    return f"SELECT * FROM {y} {s} ORDER BY {x} LIMIT {z} OFFSET {u};"

def player_details_page(player_id, season_code=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if player_id == "random":
        cursor.execute("SELECT player_id FROM euroleague_player_names")
        player_ids = cursor.fetchall()
        player_id = random.choice(player_ids)['player_id']

    cursor.execute("SELECT * FROM euroleague_player_names WHERE player_id = %s", (player_id,))
    player_name = cursor.fetchone()

    cursor.execute("""
        SELECT season_code as season, 
               SUM(games_played) as total_games_played, 
               SUM(games_started) as total_games_started, 
               ROUND(SUM(points) / NULLIF(SUM(games_played), 0), 2) AS points_per_game, 
               SUM(points) as total_points,
               ROUND(SUM(total_rebounds) / NULLIF(SUM(games_played), 0), 2) AS rebounds_per_game, 
               SUM(total_rebounds) as total_rebounds, 
               ROUND(SUM(assists) / NULLIF(SUM(games_played), 0), 2) AS assists_per_game, 
               SUM(assists) AS total_assists, 
               SUM(steals) as total_steals, 
               ROUND(SUM(steals) / NULLIF(SUM(games_played), 0), 2) AS steals_per_game, 
               ROUND(SUM(blocks_favour) / NULLIF(SUM(games_played), 0), 2) AS blocks_per_game, 
               SUM(blocks_favour) as total_blocks 
        FROM euro.euroleague_players 
        WHERE player_id = %s 
        GROUP BY season_code;
    """, (player_id,))
    all_seasons_data = cursor.fetchall()

    specific_season_data = None
    if season_code:
        cursor.execute("""
            select * from euro.euroleague_players where player_id = %s and season_code = %s;
        """, (player_id, season_code))
        specific_season_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("player_details.html", player_name=player_name, all_seasons_data=all_seasons_data, specific_season_data=specific_season_data)

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

    if team_id == "random":
        cursor.execute("SELECT team_id FROM euroleague_team_names")
        team_ids = cursor.fetchall()
        team_id = random.choice(team_ids)['team_id']

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
    page_limit = 20
    page_num = int(request.args.get('page', 1))
    page_button = 4
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM euroleague_header")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit

    if page_num < 1:
        page_num = 1
    elif page_num > page_count:
        page_num = page_count
    
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
    cursor.execute("SELECT *, euroleague_box_score.player_id AS player_id, euroleague_box_score.team_id AS team_id, CAST(euroleague_box_score.dorsal AS UNSIGNED) AS dorsal_int FROM euroleague_box_score LEFT JOIN euroleague_player_names ON euroleague_box_score.player_id = euroleague_player_names.player_id LEFT JOIN euroleague_team_names ON euroleague_box_score.team_id = euroleague_team_names.team_id WHERE game_id = %s ORDER BY euroleague_box_score.team_id ASC, dorsal_int ASC", (game_id, ))
    box_score = cursor.fetchall()
    cursor.execute("SELECT * FROM euroleague_comparison WHERE game_id = %s", (game_id, ))
    comparison = cursor.fetchone()
    cursor.execute("""SELECT *, 
                        tn.team_name AS team_name, 
                        CASE 
                            WHEN pn.player_name IS NOT NULL THEN pn.player_name
                            ELSE 'TECHNICAL'
                        END AS player_name,
                        CASE 
                            WHEN plays.quarter = 'q1' THEN 'QUARTER 1'
                            WHEN plays.quarter = 'q2' THEN 'QUARTER 2'
                            WHEN plays.quarter = 'q3' THEN 'QUARTER 3'
                            WHEN plays.quarter = 'q4' THEN 'QUARTER 4'
                            WHEN plays.quarter = 'extra_time' THEN 'OVERTIME'
                        END AS quarter_detailed,
                        (
                            SELECT COUNT(*) 
                            FROM euroleague_play_by_play plays2 
                            WHERE plays2.player_id = plays.player_id 
                            AND plays2.number_of_play <= plays.number_of_play 
                            AND plays2.game_id = plays.game_id
                        ) AS player_total_plays
                    FROM euroleague_play_by_play plays
                    LEFT JOIN euroleague_player_names pn ON plays.player_id = pn.player_id
                    LEFT JOIN euroleague_team_names tn ON plays.team_id = tn.team_id
                    LEFT JOIN euroleague_points p ON plays.game_play_id = p.game_play_id
                    WHERE game_id = %s
                    ORDER BY minute ASC, number_of_play ASC""", (game_id, ))
    play_by_play = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("match_details.html", match=match, box_score=box_score, comparison=comparison, play_by_play=play_by_play)

#sort'lar, search'ler ve pagination bozuk, düzeltilecek. overall nasıl olmalı gibi bir bakıştayız şu anda
def seasons_page():
    sort_by = request.args.get('sort_by', 'season_code asc')
    page_limit = 25
    page_num = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').strip()
    page_button = 4
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if search_query:
        where = f"WHERE player_name LIKE \"%{search_query}%\""
    else:
        where = ""
    cursor.execute("SELECT COUNT(season_code) as total FROM euroleague_header")
    entry_count = cursor.fetchone()['total']
    page_count = (entry_count + page_limit - 1) // page_limit
    cursor.execute("SELECT final_four_teams.season AS SEASON, b.team_name AS CHAMPION FROM (SELECT team_id, season, SUM(CASE WHEN points_scored > points_conceded THEN 1 ELSE 0 END) AS wins FROM (SELECT team_id_a AS team_id, score_a AS points_scored, score_b AS points_conceded, season_code AS season FROM euro.euroleague_header WHERE phase = 'FINAL FOUR' UNION ALL SELECT team_id_b AS team_id, score_b AS points_scored, score_a AS points_conceded, season_code AS season FROM euro.euroleague_header WHERE phase = 'FINAL FOUR') AS initial GROUP BY team_id, season) AS final_four_teams RIGHT JOIN euroleague_team_names b ON final_four_teams.team_id = b.team_id WHERE wins = 2 ORDER BY final_four_teams.season ASC, wins DESC;")
    season_codes = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("seasons.html", season_codes = season_codes, page_count = page_count, page_num = page_num, end_page = min(page_num + page_button, page_count))

def season_details_page(season_code):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT season_code, team_id, COUNT(*) AS games_played, SUM(CASE WHEN points_scored > points_conceded THEN 1 ELSE 0 END) AS wins, SUM(CASE WHEN points_scored < points_conceded THEN 1 ELSE 0 END) AS losses, SUM(points_scored) AS total_points_scored, SUM(points_conceded) AS total_points_conceded FROM (SELECT season_code, team_id_a AS team_id, score_a AS points_scored, score_b AS points_conceded FROM euro.euroleague_header WHERE season_code = %s UNION ALL SELECT season_code, team_id_b AS team_id, score_b AS points_scored, score_a AS points_conceded FROM euro.euroleague_header WHERE season_code = %s) AS combined_teams GROUP BY season_code, team_id ORDER BY games_played DESC, wins DESC, team_id;", (season_code, season_code,))
    season_detail = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("season_details.html", season_detail = season_detail, current_season = season_code)
