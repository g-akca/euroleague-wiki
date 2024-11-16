/*  Script Steps
    This script was written and edited during a Zoom call with all members of the team Cyclones present. We are pushing this script seperately to conform with the guidelines.
    For the respective lines, add your path to the secure file folder.
    1. Creates the Schema, Tables and Loads the data from the dataset.
    2. Alters some data to create players table.
    3. Output the current tables for future use.
    4. Create the Schema again, this time from the altered data.
    5. Modify some wrong data.
    6. Output the finalized tables.

    Initial CSV Files: https://drive.google.com/drive/folders/1cwxjZTqi8oKMayqhWs41CYwQMZiY_XJp
    Second Edition CSV Files: https://drive.google.com/drive/folders/1_8eVw5Yf7VwxuABZ3lNeoWhVFbj1GIlA
*/

/* Create the Schema*/
CREATE SCHEMA euro;
use euro;

/* Create the initial tables that will store the unmodified data from the dataset */
CREATE TABLE `euro`.`euroleague_header` (
	game_id                VARCHAR(15) NOT NULL,
	game                   VARCHAR(10) NOT NULL,
	date                   DATE NOT NULL,
	time                   TIME NOT NULL,
	round                  INTEGER  NOT NULL,
	phase                  VARCHAR(25) NOT NULL,
	season_code            VARCHAR(10) NOT NULL,
	score_a                INTEGER  NOT NULL,
	score_b                INTEGER  NOT NULL,
	team_a                 VARCHAR(50) NOT NULL,
	team_b                 VARCHAR(50) NOT NULL,
	team_id_a              VARCHAR(10) NOT NULL,
	team_id_b              VARCHAR(10) NOT NULL,
	coach_a                VARCHAR(70),
	coach_b                VARCHAR(70),
	game_time              VARCHAR(6) NOT NULL, -- mm:ss
	remaining_partial_time VARCHAR(6) NOT NULL, -- mm:ss
	referee_1              VARCHAR(70) NOT NULL,
	referee_2              VARCHAR(70) NOT NULL,
	referee_3              VARCHAR(70) NOT NULL,
	stadium                VARCHAR(70) NOT NULL,
	capacity               INTEGER  NOT NULL,
	w_id                   INTEGER  NOT NULL,
	fouls_a                INTEGER  NOT NULL,
	fouls_b                INTEGER  NOT NULL,
	timeouts_a             INTEGER  NOT NULL,
	timeouts_b             INTEGER  NOT NULL,
	score_quarter_1_a      INTEGER  NOT NULL,
	score_quarter_2_a      INTEGER  NOT NULL,
	score_quarter_3_a      INTEGER  NOT NULL,
	score_quarter_4_a      INTEGER  NOT NULL,
	score_quarter_1_b      INTEGER  NOT NULL,
	score_quarter_2_b      INTEGER  NOT NULL,
	score_quarter_3_b      INTEGER  NOT NULL,
	score_quarter_4_b      INTEGER  NOT NULL,
	score_extra_time_1_a   INTEGER,
	score_extra_time_2_a   INTEGER,
	score_extra_time_3_a   INTEGER,
	score_extra_time_4_a   INTEGER,
	score_extra_time_1_b   INTEGER,
	score_extra_time_2_b   INTEGER,
	score_extra_time_3_b   INTEGER,
	score_extra_time_4_b   INTEGER,
	PRIMARY KEY (game_id)
);

CREATE TABLE `euro`.`euroleague_points` (
	game_point_id       VARCHAR(20) NOT NULL,
	game_id             VARCHAR(15) NOT NULL,
	game                VARCHAR(10) NOT NULL,
	round               INTEGER  NOT NULL,
	phase               VARCHAR(25) NOT NULL,
	season_code         VARCHAR(10) NOT NULL,
	number_of_play      INTEGER  NOT NULL,
	team_id             VARCHAR(10) NOT NULL,
	player_id           VARCHAR(15) NOT NULL,
	player              VARCHAR(70),
	action_id           VARCHAR(10) NOT NULL,
	action              VARCHAR(30) NOT NULL,
	points              INTEGER  NOT NULL,
	coord_x             INTEGER  NOT NULL,
	coord_y             INTEGER  NOT NULL,
	zone                VARCHAR(1),
	fastbreak           INTEGER,
	second_chance       INTEGER,
	points_off_turnover INTEGER,
	minute              INTEGER  NOT NULL,
	console             VARCHAR(6) NOT NULL, -- mm:ss
	points_a            INTEGER  NOT NULL,
	points_b            INTEGER  NOT NULL,
	PRIMARY KEY (game_point_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`euroleague_teams` (
	season_team_id                  VARCHAR(15) NOT NULL,
	season_code                     VARCHAR(10) NOT NULL,
	team_id                         VARCHAR(10) NOT NULL,
	games_played                    NUMERIC(4,1) NOT NULL,
	minutes                         NUMERIC(6,1) NOT NULL,
	points                          INTEGER  NOT NULL,
	two_points_made                 INTEGER  NOT NULL,
	two_points_attempted            INTEGER  NOT NULL,
	three_points_made               INTEGER  NOT NULL,
	three_points_attempted          INTEGER  NOT NULL,
	free_throws_made                INTEGER  NOT NULL,
	free_throws_attempted           INTEGER  NOT NULL,
	offensive_rebounds              INTEGER  NOT NULL,
	defensive_rebounds              INTEGER  NOT NULL,
	total_rebounds                  INTEGER  NOT NULL,
	assists                         INTEGER  NOT NULL,
	steals                          INTEGER  NOT NULL,
	turnovers                       INTEGER  NOT NULL,
	blocks_favour                   INTEGER  NOT NULL,
	blocks_against                  INTEGER  NOT NULL,
	fouls_committed                 INTEGER  NOT NULL,
	fouls_received                  INTEGER  NOT NULL,
	valuation                       INTEGER  NOT NULL,
	minutes_per_game                NUMERIC(5,2) NOT NULL,
	points_per_game                 NUMERIC(5,2) NOT NULL,
	two_points_made_per_game        NUMERIC(5,2) NOT NULL,
	two_points_attempted_per_game   NUMERIC(5,2) NOT NULL,
	two_points_percentage           NUMERIC(5,3) NOT NULL,
	three_points_made_per_game      NUMERIC(5,2) NOT NULL,
	three_points_attempted_per_game NUMERIC(5,2) NOT NULL,
	three_points_percentage         NUMERIC(5,3) NOT NULL,
	free_throws_made_per_game       NUMERIC(5,2) NOT NULL,
	free_throws_attempted_per_game  NUMERIC(5,2) NOT NULL,
	free_throws_percentage          NUMERIC(5,3) NOT NULL,
	offensive_rebounds_per_game     NUMERIC(5,2) NOT NULL,
	defensive_rebounds_per_game     NUMERIC(5,2) NOT NULL,
	total_rebounds_per_game         NUMERIC(5,2) NOT NULL,
	assists_per_game                NUMERIC(5,2) NOT NULL,
	steals_per_game                 NUMERIC(5,2) NOT NULL,
	turnovers_per_game              NUMERIC(5,2) NOT NULL,
	blocks_favour_per_game          NUMERIC(4,2) NOT NULL,
	blocks_against_per_game         NUMERIC(4,2) NOT NULL,
	fouls_committed_per_game        NUMERIC(5,2) NOT NULL,
	fouls_received_per_game         NUMERIC(5,2) NOT NULL,
	valuation_per_game              NUMERIC(6,2) NOT NULL,
  	PRIMARY KEY (season_team_id)
);

CREATE TABLE `euro`.`euroleague_play_by_play` (
	game_play_id 			VARCHAR(20) NOT NULL,
	game_id 			VARCHAR(15) NOT NULL,
	game				VARCHAR(10) NOT NULL,
	round				INTEGER NOT NULL,
	phase				VARCHAR(25) NOT NULL,
	season_code 			VARCHAR(10) NOT NULL,
	quarter				VARCHAR(10) NOT NULL,
	type				INTEGER NOT NULL,
	number_of_play			INTEGER NOT NULL,
	team_id				VARCHAR(10),
	player_id			VARCHAR(15),
	play_type			VARCHAR(10) NOT NULL,
	player				VARCHAR(70),
	team				VARCHAR(50),
	dorsal				INTEGER,
	minute				INTEGER,
	marker_time			VARCHAR(6), -- mm:ss
	points_a			INTEGER,
	points_b			INTEGER,
    comment				VARCHAR(50),
	play_info			VARCHAR(50) NOT NULL,
	PRIMARY KEY (game_play_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`euroleague_comparison` (
	game_id				VARCHAR(15) NOT NULL,
	game				VARCHAR(10) NOT NULL,
	round				INTEGER NOT NULL,
	phase				VARCHAR(25) NOT NULL,
	season_code			VARCHAR(10) NOT NULL,
	team_id_a			VARCHAR(10) NOT NULL,
	team_id_b			VARCHAR(10) NOT NULL,
	fast_break_points_a		INTEGER NOT NULL,
	fast_break_points_b		INTEGER NOT NULL,
	turnover_points_a		INTEGER NOT NULL,
	turnover_points_b		INTEGER NOT NULL,
	second_chance_points_a	    	INTEGER NOT NULL,
	second_chance_points_b		INTEGER NOT NULL,
	defensive_rebounds_a		INTEGER NOT NULL,
	offensive_rebounds_b		INTEGER NOT NULL,
	offensive_rebounds_a	    	INTEGER NOT NULL,
	defensive_rebounds_b		INTEGER NOT NULL,
	turnovers_starters_a		INTEGER NOT NULL,
	turnovers_bench_a		INTEGER NOT NULL,
	turnovers_starters_b		INTEGER NOT NULL,
	turnovers_bench_b		INTEGER NOT NULL,
	steals_starters_a		INTEGER NOT NULL,
	steals_bench_a			INTEGER NOT NULL,
	steals_starters_b		INTEGER NOT NULL,
	steals_bench_b			INTEGER NOT NULL,
	assists_starters_a		INTEGER NOT NULL,
	assists_bench_a			INTEGER NOT NULL,
	assists_starters_b		INTEGER NOT NULL,
	assists_bench_b			INTEGER NOT NULL,
	points_starters_a		INTEGER NOT NULL,
	points_bench_a			INTEGER NOT NULL,
	points_starters_b		INTEGER NOT NULL,
	points_bench_b			INTEGER NOT NULL,
	max_a				INTEGER NOT NULL,
	minute_prev_a			INTEGER NOT NULL,
	prev_a				VARCHAR(10) NOT NULL,
	minute_str_a			INTEGER NOT NULL,
	str_a				VARCHAR(10) NOT NULL,
	max_b				INTEGER NOT NULL,
	minute_prev_b			INTEGER NOT NULL,
	prev_b				VARCHAR(10) NOT NULL,
	minute_str_b			INTEGER NOT NULL,
	str_b				VARCHAR(10) NOT NULL,
	max_lead_a			INTEGER NOT NULL,
	max_lead_b			INTEGER NOT NULL,
	minute_max_lead_a		INTEGER NOT NULL,
	minute_max_lead_b		INTEGER NOT NULL,
	points_max_lead_a		VARCHAR(10),
	points_max_lead_b		VARCHAR(10),
	PRIMARY KEY (game_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`euroleague_players`(
	season_player_id		    VARCHAR(20) NOT NULL,
	season_code                         VARCHAR(10) NOT NULL,
	player_id                           VARCHAR(15) NOT NULL,
	player                              VARCHAR(70) NOT NULL,
	team_id                             VARCHAR(10) NOT NULL,
	games_played                        NUMERIC(2) NOT NULL,
	games_started                       NUMERIC(2) NOT NULL,
	minutes                             NUMERIC(6,2) NOT NULL,
	points                              INTEGER  NOT NULL,
	two_points_made                     INTEGER  NOT NULL,
	two_points_attempted                INTEGER  NOT NULL,
	three_points_made                   INTEGER  NOT NULL,
	three_points_attempted              INTEGER  NOT NULL,
	free_throws_made                    INTEGER  NOT NULL,
	free_throws_attempted               INTEGER  NOT NULL,
	offensive_rebounds                  INTEGER  NOT NULL,
	defensive_rebounds                  INTEGER  NOT NULL,
	total_rebounds                      INTEGER  NOT NULL,
	assists                             INTEGER  NOT NULL,
	steals                              INTEGER  NOT NULL,
	turnovers                           INTEGER  NOT NULL,
	blocks_favour                       INTEGER  NOT NULL,
	blocks_against                      INTEGER  NOT NULL,
	fouls_committed                     INTEGER  NOT NULL,
	fouls_received                      INTEGER  NOT NULL,
	valuation                           INTEGER  NOT NULL,
	plus_minus                          INTEGER  NOT NULL,
	minutes_per_game                    NUMERIC(5,2) NOT NULL,
	points_per_game                     NUMERIC(5,2) NOT NULL,
	two_points_made_per_game            NUMERIC(4,2) NOT NULL,
	two_points_attempted_per_game       NUMERIC(5,2) NOT NULL,
	two_points_percentage               NUMERIC(5,3) NOT NULL,
	three_points_made_per_game          NUMERIC(4,2) NOT NULL,
	three_points_attempted_per_game     NUMERIC(4,2) NOT NULL,
	three_points_percentage             NUMERIC(5,3) NOT NULL,
	free_throws_made_per_game           NUMERIC(4,2) NOT NULL,
	free_throws_attempted_per_game      NUMERIC(4,2) NOT NULL,
	free_throws_percentage              NUMERIC(5,3) NOT NULL,
	offensive_rebounds_per_game         NUMERIC(4,2) NOT NULL,
	defensive_rebounds_per_game         NUMERIC(4,2) NOT NULL,
	total_rebounds_per_game             NUMERIC(5,2) NOT NULL,
	assists_per_game                    NUMERIC(5,2) NOT NULL,
	steals_per_game                     NUMERIC(4,2) NOT NULL,
	turnovers_per_game                  NUMERIC(4,2) NOT NULL,
	blocks_favour_per_game              NUMERIC(4,2) NOT NULL,
	blocks_against_per_game             NUMERIC(4,2) NOT NULL,
	fouls_committed_per_game            NUMERIC(4,2) NOT NULL,
	fouls_received_per_game             NUMERIC(4,2) NOT NULL,
	valuation_per_game                  NUMERIC(5,2) NOT NULL,
	plus_minus_per_game                 NUMERIC(5,2) NOT NULL,
	PRIMARY KEY (season_player_id)
);

CREATE TABLE `euro`.`euroleague_box_score`(
	game_player_id		VARCHAR(20) NOT NULL,
	game_id                 VARCHAR(15) NOT NULL,
	game                    VARCHAR(10) NOT NULL,
	round                   INTEGER  NOT NULL,
	phase                   VARCHAR(25) NOT NULL,
	season_code             VARCHAR(10) NOT NULL,
	player_id               VARCHAR(15) NOT NULL,
	is_starter              NUMERIC(3,1) NOT NULL,
	is_playing              NUMERIC(3,1) NOT NULL,
	team_id                 VARCHAR(10) NOT NULL,
	dorsal                  VARCHAR(10) NOT NULL,
	player                  VARCHAR(70) NOT NULL,
	minutes                 VARCHAR(6), -- mm:ss
	points                  INTEGER  NOT NULL,
	two_points_made         INTEGER  NOT NULL,
	two_points_attempted    INTEGER  NOT NULL,
	three_points_made       INTEGER  NOT NULL,
	three_points_attempted  INTEGER  NOT NULL,
	free_throws_made        INTEGER  NOT NULL,
	free_throws_attempted   INTEGER  NOT NULL,
	offensive_rebounds      INTEGER  NOT NULL,
	defensive_rebounds      INTEGER  NOT NULL,
	total_rebounds          INTEGER  NOT NULL,
	assists                 INTEGER  NOT NULL,
	steals                  INTEGER  NOT NULL,
	turnovers               INTEGER  NOT NULL,
	blocks_favour           INTEGER  NOT NULL,
	blocks_against          INTEGER  NOT NULL,
	fouls_committed         INTEGER  NOT NULL,
	fouls_received          INTEGER  NOT NULL,
	valuation               INTEGER  NOT NULL,
	plus_minus              INTEGER  NOT NULL,
	PRIMARY KEY (game_player_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

/* Load the data from the dataset into the tables */

set sql_mode = '';

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_header.csv'
INTO TABLE euroleague_header
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
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

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_points.csv'
INTO TABLE euroleague_points
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
SET player = NULLIF(player, ''),
	zone = NULLIF(zone, ''),
    fastbreak = NULLIF(fastbreak, ''),
    second_chance = NULLIF(second_chance, ''),
    points_off_turnover = NULLIF(points_off_turnover, '');

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_teams.csv'
INTO TABLE euroleague_teams
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_box_score.csv'
INTO TABLE euroleague_box_score
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
SET minutes = NULLIF(minutes, '');
    
LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_players.csv'
INTO TABLE euroleague_players
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_play_by_play.csv'
INTO TABLE euroleague_play_by_play
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
SET team_id = NULLIF(team_id, ''),
	player_id = NULLIF(player_id, ''),
	player = NULLIF(player, ''),
	team = NULLIF(team, ''),
	dorsal = NULLIF(dorsal, ''),
	marker_time = NULLIF(marker_time, ''),
	points_a = NULLIF(points_a, ''),
	points_b = NULLIF(points_b, '');

LOAD DATA INFILE 'D:/MySQL/Uploads/euroleague_comparison.csv'
INTO TABLE euroleague_comparison
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
SET points_max_lead_a = NULLIF(points_max_lead_a, ''),
	points_max_lead_b = NULLIF(points_max_lead_b, '');
    
/* DATA CORRECTION | there are 2 players that change player_id between seasons, we altered the data so that we can create a players table */

UPDATE euroleague_players
SET season_player_id = 'E2023_P011974_PAM'
WHERE season_player_id = 'E2023_P010754_PAM';

UPDATE euroleague_players
SET player_id = 'P011974'
WHERE season_player_id = 'E2023_P011974_PAM';

UPDATE euroleague_players
SET season_player_id = 'E2023_PLRU_RED'
WHERE season_player_id = 'E2023_P012711_RED';

UPDATE euroleague_players
SET player_id = 'PLRU'
WHERE season_player_id = 'E2023_PLRU_RED';   

ALTER TABLE euroleague_play_by_play DROP COLUMN `comment`;
    
/* export the tables with the corrected player ids, the results of the exports will be used for finalized tables. (Some initial tables have unnnecessary data) */

SELECT 'game_id', 'game', 'date', 'time', 'round', 'phase', 'season_code', 'score_a', 'score_b', 'team_a', 'team_b', 'team_id_a', 'team_id_b', 'coach_a', 'coach_b', 'game_time', 'remaining_partial_time', 'referee_1', 'referee_2', 'referee_3', 'stadium', 'capacity', 'w_id', 'fouls_a', 'fouls_b', 'timeouts_a', 'timeouts_b', 'score_quarter_1_a', 'score_quarter_2_a', 'score_quarter_3_a', 'score_quarter_4_a', 'score_quarter_1_b', 'score_quarter_2_b', 'score_quarter_3_b', 'score_quarter_4_b', 'score_extra_time_1_a', 'score_extra_time_2_a', 'score_extra_time_3_a', 'score_extra_time_4_a', 'score_extra_time_1_b', 'score_extra_time_2_b', 'score_extra_time_3_b', 'score_extra_time_4_b'
UNION all
SELECT game_id, game, date, time, round, phase, season_code, score_a, score_b, team_a, team_b, team_id_a, team_id_b, IFNULL(coach_a, ''), IFNULL(coach_b, ''), game_time, remaining_partial_time, referee_1, referee_2, referee_3, stadium, capacity, w_id, fouls_a, fouls_b, timeouts_a, timeouts_b, score_quarter_1_a, score_quarter_2_a, score_quarter_3_a, score_quarter_4_a, score_quarter_1_b, score_quarter_2_b, score_quarter_3_b, score_quarter_4_b, IFNULL(score_extra_time_1_a, ''), IFNULL(score_extra_time_2_a, ''), IFNULL(score_extra_time_3_a, ''), IFNULL(score_extra_time_4_a, ''), IFNULL(score_extra_time_1_b, ''), IFNULL(score_extra_time_2_b, ''), IFNULL(score_extra_time_3_b, ''), IFNULL(score_extra_time_4_b, '')
FROM euroleague_header
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_header2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'game_play_id', 'game_id', 'quarter', 'number_of_play', 'team_id', 'player_id', 'play_type', 'team', 'dorsal', 'minute', 'marker_time', 'play_info'
UNION all
SELECT game_play_id, game_id, quarter, number_of_play, IFNULL(team_id, ''), IFNULL(player_id, ''), play_type, IFNULL(team, ''), IFNULL(dorsal, ''), minute, IFNULL(marker_time, ''), play_info
FROM euroleague_play_by_play
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_play_by_play2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'points_primary_id', 'game_point_id', 'action', 'points', 'coord_x', 'coord_y', 'zone', 'fastbreak', 'second_chance', 'points_off_turnover', 'points_a', 'points_b'
UNION all
SELECT NULL, game_point_id, action, points, coord_x, coord_y, IFNULL(zone, ''), IFNULL(fastbreak, ''), IFNULL(second_chance, ''), IFNULL(points_off_turnover, ''), points_a, points_b
FROM euroleague_points
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_points2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'season_team_id', 'season_code', 'team_id', 'games_played', 'minutes', 'points', 'two_points_made', 'two_points_attempted', 'three_points_made', 'three_points_attempted', 'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against', 'fouls_committed', 'fouls_received', 'valuation', 'minutes_per_game', 'points_per_game', 'two_points_made_per_game', 'two_points_attempted_per_game', 'two_points_percentage', 'three_points_made_per_game', 'three_points_attempted_per_game', 'three_points_percentage', 'free_throws_made_per_game', 'free_throws_attempted_per_game', 'free_throws_percentage', 'offensive_rebounds_per_game', 'defensive_rebounds_per_game', 'total_rebounds_per_game', 'assists_per_game', 'steals_per_game', 'turnovers_per_game', 'blocks_favour_per_game', 'blocks_against_per_game', 'fouls_committed_per_game', 'fouls_received_per_game', 'valuation_per_game'
UNION all
SELECT *
FROM euroleague_teams
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_teams2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'player_id', 'player'
UNION all
SELECT DISTINCT(player_id), player
FROM euroleague_players
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_player_names2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'season_player_id', 'season_code', 'player_id', 'team_id', 'games_played', 'games_started', 'minutes', 'points', 'two_points_made', 'two_points_attempted', 'three_points_made', 'three_points_attempted', 'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against', 'fouls_committed', 'fouls_received', 'valuation', 'plus_minus', 'minutes_per_game', 'points_per_game', 'two_points_made_per_game', 'two_points_attempted_per_game', 'two_points_percentage', 'three_points_made_per_game', 'three_points_attempted_per_game', 'three_points_percentage', 'free_throws_made_per_game', 'free_throws_attempted_per_game', 'free_throws_percentage', 'offensive_rebounds_per_game', 'defensive_rebounds_per_game', 'total_rebounds_per_game', 'assists_per_game', 'steals_per_game', 'turnovers_per_game', 'blocks_favour_per_game', 'blocks_against_per_game', 'fouls_committed_per_game', 'fouls_received_per_game', 'valuation_per_game', 'plus_minus_per_game'
UNION all 
SELECT IFNULL(season_player_id, ''), IFNULL(season_code, ''), IFNULL(player_id, ''), IFNULL(team_id, ''), IFNULL(games_played, ''), IFNULL(games_started, ''), IFNULL(minutes, ''), IFNULL(points, ''), IFNULL(two_points_made, ''), IFNULL(two_points_attempted, ''), IFNULL(three_points_made, ''), IFNULL(three_points_attempted, ''), IFNULL(free_throws_made, ''), IFNULL(free_throws_attempted, ''), IFNULL(offensive_rebounds, ''), IFNULL(defensive_rebounds, ''), IFNULL(total_rebounds, ''), IFNULL(assists, ''), IFNULL(steals, ''), IFNULL(turnovers, ''), IFNULL(blocks_favour, ''), IFNULL(blocks_against, ''), IFNULL(fouls_committed, ''), IFNULL(fouls_received, ''), IFNULL(valuation, ''), IFNULL(plus_minus, ''), IFNULL(minutes_per_game, ''), IFNULL(points_per_game, ''), IFNULL(two_points_made_per_game, ''), IFNULL(two_points_attempted_per_game, ''), IFNULL(two_points_percentage, ''), IFNULL(three_points_made_per_game, ''), IFNULL(three_points_attempted_per_game, ''), IFNULL(three_points_percentage, ''), IFNULL(free_throws_made_per_game, ''), IFNULL(free_throws_attempted_per_game, ''), IFNULL(free_throws_percentage, ''), IFNULL(offensive_rebounds_per_game, ''), IFNULL(defensive_rebounds_per_game, ''), IFNULL(total_rebounds_per_game, ''), IFNULL(assists_per_game, ''), IFNULL(steals_per_game, ''), IFNULL(turnovers_per_game, ''), IFNULL(blocks_favour_per_game, ''), IFNULL(blocks_against_per_game, ''), IFNULL(fouls_committed_per_game, ''), IFNULL(fouls_received_per_game, ''), IFNULL(valuation_per_game, ''), IFNULL(plus_minus_per_game, '')
FROM euroleague_players
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_players2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'game_player_id', 'game_id', 'player_id', 'is_starter', 'is_playing', 'team_id', 'dorsal', 'minutes', 'points', 'two_points_made', 'two_points_attempted', 'three_points_made', 'three_points_attempted', 'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against', 'fouls_committed', 'fouls_received', 'valuation', 'plus_minus'
UNION all
SELECT game_player_id, game_id, player_id, is_starter, is_playing, team_id, dorsal, IFNULL(minutes, ''), points, two_points_made, two_points_attempted, three_points_made, three_points_attempted, free_throws_made, free_throws_attempted, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, turnovers, blocks_favour, blocks_against, fouls_committed, fouls_received, valuation, plus_minus
FROM euroleague_box_score
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_box_score2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

SELECT 'game_id', 'fast_break_points_a', 'fast_break_points_b', 'turnover_points_a', 'turnover_points_b', 'second_chance_points_a', 'second_chance_points_b', 'defensive_rebounds_a', 'offensive_rebounds_b', 'offensive_rebounds_a', 'defensive_rebounds_b', 'turnovers_starters_a', 'turnovers_bench_a', 'turnovers_starters_b', 'turnovers_bench_b', 'steals_starters_a', 'steals_bench_a', 'steals_starters_b', 'steals_bench_b', 'assists_starters_a', 'assists_bench_a', 'assists_starters_b', 'assists_bench_b', 'points_starters_a', 'points_bench_a', 'points_starters_b', 'points_bench_b', 'max_a', 'minute_prev_a', 'prev_a', 'minute_str_a', 'str_a', 'max_b', 'minute_prev_b', 'prev_b', 'minute_str_b', 'str_b', 'max_lead_a', 'max_lead_b', 'minute_max_lead_a', 'minute_max_lead_b', 'points_max_lead_a', 'points_max_lead_b'
UNION all
SELECT game_id, fast_break_points_a, fast_break_points_b, turnover_points_a, turnover_points_b, second_chance_points_a, second_chance_points_b, defensive_rebounds_a, offensive_rebounds_b, offensive_rebounds_a, defensive_rebounds_b, turnovers_starters_a, turnovers_bench_a, turnovers_starters_b, turnovers_bench_b, steals_starters_a, steals_bench_a, steals_starters_b, steals_bench_b, assists_starters_a, assists_bench_a, assists_starters_b, assists_bench_b, points_starters_a, points_bench_a, points_starters_b, points_bench_b, max_a, minute_prev_a, prev_a, minute_str_a, str_a, max_b, minute_prev_b, prev_b, minute_str_b, str_b, max_lead_a, max_lead_b, minute_max_lead_a, minute_max_lead_b, IFNULL(points_max_lead_a, ''), IFNULL(points_max_lead_b, '')
FROM euroleague_comparison
INTO OUTFILE 'D:/MySQL/Uploads/euroleague_comparison2.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\r';

/* Create the schema and tables that will be used with modified data */

DROP SCHEMA euro;
CREATE SCHEMA euro;
use euro;

CREATE TABLE `euro`.`euroleague_header` (
	game_id                VARCHAR(15) NOT NULL,
	game                   VARCHAR(10) NOT NULL,
	date                   DATE NOT NULL,
	time                   TIME NOT NULL,
	round                  INTEGER  NOT NULL,
	phase                  VARCHAR(25) NOT NULL,
	season_code            VARCHAR(10) NOT NULL,
	score_a                INTEGER  NOT NULL,
	score_b                INTEGER  NOT NULL,
    team_a                 VARCHAR(50) NOT NULL,
	team_b                 VARCHAR(50) NOT NULL,
	team_id_a              VARCHAR(10) NOT NULL,
	team_id_b              VARCHAR(10) NOT NULL,
	coach_a                VARCHAR(70),
	coach_b                VARCHAR(70),
	game_time              VARCHAR(6) NOT NULL, -- mm:ss
	remaining_partial_time VARCHAR(6) NOT NULL, -- mm:ss
	referee_1              VARCHAR(70) NOT NULL,
	referee_2              VARCHAR(70) NOT NULL,
	referee_3              VARCHAR(70) NOT NULL,
	stadium                VARCHAR(70) NOT NULL,
	capacity               INTEGER  NOT NULL,
	w_id                   INTEGER  NOT NULL,
	fouls_a                INTEGER  NOT NULL,
	fouls_b                INTEGER  NOT NULL,
	timeouts_a             INTEGER  NOT NULL,
	timeouts_b             INTEGER  NOT NULL,
	score_quarter_1_a      INTEGER  NOT NULL,
	score_quarter_2_a      INTEGER  NOT NULL,
	score_quarter_3_a      INTEGER  NOT NULL,
	score_quarter_4_a      INTEGER  NOT NULL,
	score_quarter_1_b      INTEGER  NOT NULL,
	score_quarter_2_b      INTEGER  NOT NULL,
	score_quarter_3_b      INTEGER  NOT NULL,
	score_quarter_4_b      INTEGER  NOT NULL,
	score_extra_time_1_a   INTEGER,
	score_extra_time_2_a   INTEGER,
	score_extra_time_3_a   INTEGER,
	score_extra_time_4_a   INTEGER,
	score_extra_time_1_b   INTEGER,
	score_extra_time_2_b   INTEGER,
	score_extra_time_3_b   INTEGER,
	score_extra_time_4_b   INTEGER,
    PRIMARY KEY (game_id)
);

CREATE TABLE `euro`.`euroleague_play_by_play` (
	game_play_id 		VARCHAR(20) NOT NULL,
	game_id 			VARCHAR(15) NOT NULL,
	quarter				VARCHAR(10) NOT NULL,
	number_of_play		INTEGER NOT NULL,
	team_id				VARCHAR(10),
	player_id			VARCHAR(15),
	play_type			VARCHAR(10) NOT NULL,
    team				VARCHAR(50),
	dorsal				INTEGER,
	minute				INTEGER,
	marker_time			VARCHAR(6), -- mm:ss
	play_info			VARCHAR(50) NOT NULL,
	PRIMARY KEY (game_play_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`euroleague_points` (
	points_primary_id 	INTEGER NOT NULL AUTO_INCREMENT,
	game_point_id       VARCHAR(20) NOT NULL,
	action              VARCHAR(30) NOT NULL,
	points              INTEGER  NOT NULL,
	coord_x             INTEGER  NOT NULL,
	coord_y             INTEGER  NOT NULL,
	zone                VARCHAR(1),
	fastbreak           INTEGER,
	second_chance       INTEGER,
	points_off_turnover INTEGER,
	points_a            INTEGER  NOT NULL,
	points_b            INTEGER  NOT NULL,
    PRIMARY KEY (points_primary_id),
	FOREIGN KEY (game_point_id) REFERENCES euroleague_play_by_play(game_play_id)
);

CREATE TABLE `euro`.`euroleague_teams` (
	season_team_id                  VARCHAR(15) NOT NULL,
	season_code                     VARCHAR(10) NOT NULL,
	team_id                         VARCHAR(10) NOT NULL,
	games_played                    NUMERIC(4,1) NOT NULL,
	minutes                         NUMERIC(6,1) NOT NULL,
	points                          INTEGER  NOT NULL,
	two_points_made                 INTEGER  NOT NULL,
	two_points_attempted            INTEGER  NOT NULL,
	three_points_made               INTEGER  NOT NULL,
	three_points_attempted          INTEGER  NOT NULL,
	free_throws_made                INTEGER  NOT NULL,
	free_throws_attempted           INTEGER  NOT NULL,
	offensive_rebounds              INTEGER  NOT NULL,
	defensive_rebounds              INTEGER  NOT NULL,
	total_rebounds                  INTEGER  NOT NULL,
	assists                         INTEGER  NOT NULL,
	steals                          INTEGER  NOT NULL,
	turnovers                       INTEGER  NOT NULL,
	blocks_favour                   INTEGER  NOT NULL,
	blocks_against                  INTEGER  NOT NULL,
	fouls_committed                 INTEGER  NOT NULL,
	fouls_received                  INTEGER  NOT NULL,
	valuation                       INTEGER  NOT NULL,
	minutes_per_game                NUMERIC(5,2) NOT NULL,
	points_per_game                 NUMERIC(5,2) NOT NULL,
	two_points_made_per_game        NUMERIC(5,2) NOT NULL,
	two_points_attempted_per_game   NUMERIC(5,2) NOT NULL,
	two_points_percentage           NUMERIC(5,3) NOT NULL,
	three_points_made_per_game      NUMERIC(5,2) NOT NULL,
	three_points_attempted_per_game NUMERIC(5,2) NOT NULL,
	three_points_percentage         NUMERIC(5,3) NOT NULL,
	free_throws_made_per_game       NUMERIC(5,2) NOT NULL,
	free_throws_attempted_per_game  NUMERIC(5,2) NOT NULL,
	free_throws_percentage          NUMERIC(5,3) NOT NULL,
	offensive_rebounds_per_game     NUMERIC(5,2) NOT NULL,
	defensive_rebounds_per_game     NUMERIC(5,2) NOT NULL,
	total_rebounds_per_game         NUMERIC(5,2) NOT NULL,
	assists_per_game                NUMERIC(5,2) NOT NULL,
	steals_per_game                 NUMERIC(5,2) NOT NULL,
	turnovers_per_game              NUMERIC(5,2) NOT NULL,
	blocks_favour_per_game          NUMERIC(4,2) NOT NULL,
	blocks_against_per_game         NUMERIC(4,2) NOT NULL,
	fouls_committed_per_game        NUMERIC(5,2) NOT NULL,
	fouls_received_per_game         NUMERIC(5,2) NOT NULL,
	valuation_per_game              NUMERIC(6,2) NOT NULL,
    PRIMARY KEY (season_team_id)
);

CREATE TABLE `euro`.`euroleague_player_names`(
	player_id                           VARCHAR(15) NOT NULL,
	player_name                         VARCHAR(70) NOT NULL,
	PRIMARY KEY (player_id)
);

CREATE TABLE `euro`.`euroleague_players`(
	season_player_id					VARCHAR(20) NOT NULL,
	season_code                         VARCHAR(10) NOT NULL,
	player_id                           VARCHAR(15) NOT NULL,
	team_id                             VARCHAR(10) NOT NULL,
	games_played                        NUMERIC(2) NOT NULL,
	games_started                       NUMERIC(2) NOT NULL,
	minutes                             NUMERIC(6,2) NOT NULL,
	points                              INTEGER  NOT NULL,
	two_points_made                     INTEGER  NOT NULL,
	two_points_attempted                INTEGER  NOT NULL,
	three_points_made                   INTEGER  NOT NULL,
	three_points_attempted              INTEGER  NOT NULL,
	free_throws_made                    INTEGER  NOT NULL,
	free_throws_attempted               INTEGER  NOT NULL,
	offensive_rebounds                  INTEGER  NOT NULL,
	defensive_rebounds                  INTEGER  NOT NULL,
	total_rebounds                      INTEGER  NOT NULL,
	assists                             INTEGER  NOT NULL,
	steals                              INTEGER  NOT NULL,
	turnovers                           INTEGER  NOT NULL,
	blocks_favour                       INTEGER  NOT NULL,
	blocks_against                      INTEGER  NOT NULL,
	fouls_committed                     INTEGER  NOT NULL,
	fouls_received                      INTEGER  NOT NULL,
	valuation                           INTEGER  NOT NULL,
	plus_minus                          INTEGER  NOT NULL,
	minutes_per_game                    NUMERIC(5,2) NOT NULL,
	points_per_game                     NUMERIC(5,2) NOT NULL,
	two_points_made_per_game            NUMERIC(4,2) NOT NULL,
	two_points_attempted_per_game       NUMERIC(5,2) NOT NULL,
	two_points_percentage               NUMERIC(5,3) NOT NULL,
	three_points_made_per_game          NUMERIC(4,2) NOT NULL,
	three_points_attempted_per_game     NUMERIC(4,2) NOT NULL,
	three_points_percentage             NUMERIC(5,3) NOT NULL,
	free_throws_made_per_game           NUMERIC(4,2) NOT NULL,
	free_throws_attempted_per_game      NUMERIC(4,2) NOT NULL,
	free_throws_percentage              NUMERIC(5,3) NOT NULL,
	offensive_rebounds_per_game         NUMERIC(4,2) NOT NULL,
	defensive_rebounds_per_game         NUMERIC(4,2) NOT NULL,
	total_rebounds_per_game             NUMERIC(5,2) NOT NULL,
	assists_per_game                    NUMERIC(5,2) NOT NULL,
	steals_per_game                     NUMERIC(4,2) NOT NULL,
	turnovers_per_game                  NUMERIC(4,2) NOT NULL,
	blocks_favour_per_game              NUMERIC(4,2) NOT NULL,
	blocks_against_per_game             NUMERIC(4,2) NOT NULL,
	fouls_committed_per_game            NUMERIC(4,2) NOT NULL,
	fouls_received_per_game             NUMERIC(4,2) NOT NULL,
	valuation_per_game                  NUMERIC(5,2) NOT NULL,
	plus_minus_per_game                 NUMERIC(5,2) NOT NULL,
	PRIMARY KEY (season_player_id),
    FOREIGN KEY (player_id) REFERENCES euroleague_player_names(player_id)
);

CREATE TABLE `euro`.`euroleague_box_score`(
	game_player_id			VARCHAR(20) NOT NULL ,
	game_id                 VARCHAR(15) NOT NULL,
	player_id               VARCHAR(15) NOT NULL,
	is_starter              NUMERIC(3,1) NOT NULL,
	is_playing              NUMERIC(3,1) NOT NULL,
	team_id                 VARCHAR(10) NOT NULL,
	dorsal                  VARCHAR(10) NOT NULL,
	minutes                 VARCHAR(6), -- mm:ss
	points                  INTEGER  NOT NULL,
	two_points_made         INTEGER  NOT NULL,
	two_points_attempted    INTEGER  NOT NULL,
	three_points_made       INTEGER  NOT NULL,
	three_points_attempted  INTEGER  NOT NULL,
	free_throws_made        INTEGER  NOT NULL,
	free_throws_attempted   INTEGER  NOT NULL,
	offensive_rebounds      INTEGER  NOT NULL,
	defensive_rebounds      INTEGER  NOT NULL,
	total_rebounds          INTEGER  NOT NULL,
	assists                 INTEGER  NOT NULL,
	steals                  INTEGER  NOT NULL,
	turnovers               INTEGER  NOT NULL,
	blocks_favour           INTEGER  NOT NULL,
	blocks_against          INTEGER  NOT NULL,
	fouls_committed         INTEGER  NOT NULL,
	fouls_received          INTEGER  NOT NULL,
	valuation               INTEGER  NOT NULL,
	plus_minus              INTEGER  NOT NULL,
	PRIMARY KEY (game_player_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`euroleague_comparison` (
	game_id						VARCHAR(15) NOT NULL,
	fast_break_points_a			INTEGER NOT NULL,
	fast_break_points_b			INTEGER NOT NULL,
	turnover_points_a			INTEGER NOT NULL,
	turnover_points_b			INTEGER NOT NULL,
	second_chance_points_a	    INTEGER NOT NULL,
	second_chance_points_b		INTEGER NOT NULL,
	defensive_rebounds_a		INTEGER NOT NULL,
	offensive_rebounds_b		INTEGER NOT NULL,
	offensive_rebounds_a	    INTEGER NOT NULL,
	defensive_rebounds_b		INTEGER NOT NULL,
	turnovers_starters_a		INTEGER NOT NULL,
	turnovers_bench_a			INTEGER NOT NULL,
	turnovers_starters_b		INTEGER NOT NULL,
	turnovers_bench_b			INTEGER NOT NULL,
	steals_starters_a			INTEGER NOT NULL,
	steals_bench_a				INTEGER NOT NULL,
	steals_starters_b			INTEGER NOT NULL,
	steals_bench_b				INTEGER NOT NULL,
	assists_starters_a			INTEGER NOT NULL,
	assists_bench_a				INTEGER NOT NULL,
	assists_starters_b			INTEGER NOT NULL,
	assists_bench_b				INTEGER NOT NULL,
	points_starters_a			INTEGER NOT NULL,
	points_bench_a				INTEGER NOT NULL,
	points_starters_b			INTEGER NOT NULL,
	points_bench_b				INTEGER NOT NULL,
	max_a						INTEGER NOT NULL,
	minute_prev_a				INTEGER NOT NULL,
	prev_a						VARCHAR(10) NOT NULL,
	minute_str_a				INTEGER NOT NULL,
	str_a						VARCHAR(10) NOT NULL,
	max_b						INTEGER NOT NULL,
	minute_prev_b				INTEGER NOT NULL,
	prev_b						VARCHAR(10) NOT NULL,
	minute_str_b				INTEGER NOT NULL,
	str_b						VARCHAR(10) NOT NULL,
	max_lead_a					INTEGER NOT NULL,
	max_lead_b					INTEGER NOT NULL,
	minute_max_lead_a			INTEGER NOT NULL,
	minute_max_lead_b			INTEGER NOT NULL,
	points_max_lead_a			VARCHAR(10),
	points_max_lead_b			VARCHAR(10),
	PRIMARY KEY (game_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`users` (
	user_id			INTEGER NOT NULL AUTO_INCREMENT,
    username		VARCHAR(20) NOT NULL UNIQUE,
    email			VARCHAR(100) NOT NULL UNIQUE CHECK(email LIKE '%@%'),
    password		VARCHAR(25) NOT NULL,
    role			CHAR(1) DEFAULT 'U',
    register_time	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

/* Create an admin account with the username "admin" and password "cyclones" */
INSERT INTO euro.users (username, email, password, role)
VALUES ('admin', 'admin@email.com', 'cyclones', 'A');

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
