/* Load the data from the modified csv files. */

set sql_mode = '';

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_header2.csv'
INTO TABLE euroleague_header
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS
SET coach_a = NULLIF(coach_a, ''),
	coach_b = NULLIF(coach_b, ''),
    score_extra_time_1_a = NULLIF(score_extra_time_1_a, ''),
    score_extra_time_2_a = NULLIF(score_extra_time_2_a, ''),
    score_extra_time_3_a = NULLIF(score_extra_time_3_a, ''),
    score_extra_time_4_a = NULLIF(score_extra_time_4_a, ''),
    score_extra_time_1_b = NULLIF(score_extra_time_1_b, ''),
    score_extra_time_2_b = NULLIF(score_extra_time_2_b, ''),
    score_extra_time_3_b = NULLIF(score_extra_time_3_b, ''),
    score_extra_time_4_b = NULLIF(score_extra_time_4_b, '');
    
LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_play_by_play2.csv'
INTO TABLE euroleague_play_by_play
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS
SET team_id = NULLIF(team_id, ''),
	player_id = NULLIF(player_id, ''),
    team = NULLIF(team, ''),
	dorsal = NULLIF(dorsal, ''),
	marker_time = NULLIF(marker_time, '');

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_points2.csv'
INTO TABLE euroleague_points
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS
SET zone = NULLIF(zone, ''),
    fastbreak = NULLIF(fastbreak, ''),
    second_chance = NULLIF(second_chance, ''),
    points_off_turnover = NULLIF(points_off_turnover, '');

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_teams2.csv'
INTO TABLE euroleague_teams
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;
    
LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_player_names2.csv'
INTO TABLE euroleague_player_names
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_players2.csv'
INTO TABLE euroleague_players
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_box_score2.csv'
INTO TABLE euroleague_box_score
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS
SET minutes = NULLIF(minutes, '');

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_comparison2.csv'
INTO TABLE euroleague_comparison
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r'
IGNORE 1 ROWS
SET points_max_lead_a = NULLIF(points_max_lead_a, ''),
	points_max_lead_b = NULLIF(points_max_lead_b, '');

/* DATA CORRECTION - After creating a new table called euroleague_player_names, modify the previously wrong player_id's. */
UPDATE euro.euroleague_box_score
SET game_player_id = 'E2023_026_P011974'
WHERE game_id = 'E2023_026' and player_id = 'P010754';

UPDATE euro.euroleague_box_score
SET game_player_id = 'E2023_032_P011974'
WHERE game_id = 'E2023_032' and player_id = 'P010754';

UPDATE euro.euroleague_box_score
SET player_id = 'P011974'
WHERE game_player_id = 'E2023_032_P011974';

UPDATE euro.euroleague_box_score
SET player_id = 'P011974'
WHERE game_player_id = 'E2023_026_P011974';

UPDATE euro.euroleague_box_score
SET game_player_id = CONCAT(game_id, '_PLKU')
WHERE player_id = 'P012711';

UPDATE euro.euroleague_box_score
SET player_id = 'PLKU'
WHERE player_id = 'P012711';

UPDATE euro.euroleague_play_by_play
SET player_id = 'PLKU'
WHERE player_id = 'P012711';

UPDATE euro.euroleague_play_by_play
SET player_id = 'P011974'
WHERE player_id = 'P010754';

/* Export the finalized data that will be used for the project. */

SELECT 'game_id', 'game', 'date', 'time', 'round', 'phase', 'season_code', 'score_a', 'score_b', 'team_a', 'team_b', 'team_id_a', 'team_id_b', 'coach_a', 'coach_b', 'game_time', 'remaining_partial_time', 'referee_1', 'referee_2', 'referee_3', 'stadium', 'capacity', 'w_id', 'fouls_a', 'fouls_b', 'timeouts_a', 'timeouts_b', 'score_quarter_1_a', 'score_quarter_2_a', 'score_quarter_3_a', 'score_quarter_4_a', 'score_quarter_1_b', 'score_quarter_2_b', 'score_quarter_3_b', 'score_quarter_4_b', 'score_extra_time_1_a', 'score_extra_time_2_a', 'score_extra_time_3_a', 'score_extra_time_4_a', 'score_extra_time_1_b', 'score_extra_time_2_b', 'score_extra_time_3_b', 'score_extra_time_4_b'
UNION all
SELECT *
FROM euroleague_header
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_header_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'game_play_id', 'game_id', 'quarter', 'number_of_play', 'team_id', 'player_id', 'play_type', 'team', 'dorsal', 'minute', 'marker_time', 'play_info'
UNION all
SELECT *
FROM euroleague_play_by_play
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_play_by_play_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'primary_point_id', 'game_play_id', 'action', 'points', 'coord_x', 'coord_y', 'zone', 'fastbreak', 'second_chance', 'points_off_turnover', 'points_a', 'points_b'
UNION all
SELECT *
FROM euroleague_points
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_points_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'season_team_id', 'season_code', 'team_id', 'games_played', 'minutes', 'points', 'two_points_made', 'two_points_attempted', 'three_points_made', 'three_points_attempted', 'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against', 'fouls_committed', 'fouls_received', 'valuation', 'minutes_per_game', 'points_per_game', 'two_points_made_per_game', 'two_points_attempted_per_game', 'two_points_percentage', 'three_points_made_per_game', 'three_points_attempted_per_game', 'three_points_percentage', 'free_throws_made_per_game', 'free_throws_attempted_per_game', 'free_throws_percentage', 'offensive_rebounds_per_game', 'defensive_rebounds_per_game', 'total_rebounds_per_game', 'assists_per_game', 'steals_per_game', 'turnovers_per_game', 'blocks_favour_per_game', 'blocks_against_per_game', 'fouls_committed_per_game', 'fouls_received_per_game', 'valuation_per_game'
UNION all
SELECT *
FROM euroleague_teams
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_teams_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'player_id', 'player_name'
UNION all
SELECT *
FROM euroleague_player_names
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_player_names_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'season_player_id', 'season_code', 'player_id', 'team_id', 'games_played', 'games_started', 'minutes', 'points', 'two_points_made', 'two_points_attempted', 'three_points_made', 'three_points_attempted', 'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against', 'fouls_committed', 'fouls_received', 'valuation', 'plus_minus', 'minutes_per_game', 'points_per_game', 'two_points_made_per_game', 'two_points_attempted_per_game', 'two_points_percentage', 'three_points_made_per_game', 'three_points_attempted_per_game', 'three_points_percentage', 'free_throws_made_per_game', 'free_throws_attempted_per_game', 'free_throws_percentage', 'offensive_rebounds_per_game', 'defensive_rebounds_per_game', 'total_rebounds_per_game', 'assists_per_game', 'steals_per_game', 'turnovers_per_game', 'blocks_favour_per_game', 'blocks_against_per_game', 'fouls_committed_per_game', 'fouls_received_per_game', 'valuation_per_game', 'plus_minus_per_game'
UNION all
SELECT *
FROM euroleague_players
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_players_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'game_player_id', 'game_id', 'player_id', 'is_starter', 'is_playing', 'team_id', 'dorsal', 'minutes', 'points', 'two_points_made', 'two_points_attempted', 'three_points_made', 'three_points_attempted', 'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against', 'fouls_committed', 'fouls_received', 'valuation', 'plus_minus'
UNION all
SELECT *
FROM euroleague_box_score
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_box_score_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'game_id', 'fast_break_points_a', 'fast_break_points_b', 'turnover_points_a', 'turnover_points_b', 'second_chance_points_a', 'second_chance_points_b', 'defensive_rebounds_a', 'offensive_rebounds_b', 'offensive_rebounds_a', 'defensive_rebounds_b', 'turnovers_starters_a', 'turnovers_bench_a', 'turnovers_starters_b', 'turnovers_bench_b', 'steals_starters_a', 'steals_bench_a', 'steals_starters_b', 'steals_bench_b', 'assists_starters_a', 'assists_bench_a', 'assists_starters_b', 'assists_bench_b', 'points_starters_a', 'points_bench_a', 'points_starters_b', 'points_bench_b', 'max_a', 'minute_prev_a', 'prev_a', 'minute_str_a', 'str_a', 'max_b', 'minute_prev_b', 'prev_b', 'minute_str_b', 'str_b', 'max_lead_a', 'max_lead_b', 'minute_max_lead_a', 'minute_max_lead_b', 'points_max_lead_a', 'points_max_lead_b'
UNION all
SELECT *
FROM euroleague_comparison
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_comparison_final.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';
