-- This is a script for the creation of the schema and the tables.

/* 1. Creating the schema and using it*/
CREATE SCHEMA euro;
use euro;

/* 2. Creating the tables */
CREATE TABLE `euro`.`euroleague_header` ( /* Gökçe */
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

CREATE TABLE `euro`.`euroleague_points` ( /* Gökçe */
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

CREATE TABLE `euro`.`euroleague_teams` ( /* Gökçe */
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

CREATE TABLE `euro`.`euroleague_play_by_play` ( /* Eren */
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
	play_info			VARCHAR(50) NOT NULL,
	PRIMARY KEY (game_play_id),
	FOREIGN KEY (game_id) REFERENCES euroleague_header(game_id)
);

CREATE TABLE `euro`.`euroleague_comparison` ( /* Eren */
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

CREATE TABLE `euro`.`euroleague_players`( /* Ege */
	season_player_id		    VARCHAR(20) NOT NULL,
	season_code                         VARCHAR(10) NOT NULL,
	player_id                           VARCHAR(15) NOT NULL,
	player                              VARCHAR(70) NOT NULL,
	team_id                             VARCHAR(10) NOT NULL,
	games_played                        NUMERIC(2) NOT NULL,
	games_started                       NUMERIC(2) NOT NULL,
	minutes                             NUMERIC(6,4) NOT NULL,
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

CREATE TABLE `euro`.`euroleague_box_score`( /* Ege */
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
