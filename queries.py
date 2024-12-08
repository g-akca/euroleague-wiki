play_by_play_query = """
    SELECT 
        header.date, 
        ADDTIME(header.time, SEC_TO_TIME(play.minute * 60)) AS play_time,
        header.game, 
        play.team, 
        player.player_name,
        CASE 
            WHEN play.quarter = 'q1' THEN 'Quarter 1'
            WHEN play.quarter = 'q2' THEN 'Quarter 2'
            WHEN play.quarter = 'q3' THEN 'Quarter 3'
            WHEN play.quarter = 'q4' THEN 'Quarter 4'
            WHEN play.quarter = 'extra_time' THEN 'Overtime'
            ELSE 'Unknown'
        END AS quarter_description,
        play.play_type
    FROM euroleague_play_by_play AS play
    JOIN euroleague_header AS header
    ON play.game_id = header.game_id
    JOIN euroleague_player_names AS player
    ON play.player_id = player.player_id
    LIMIT 100;
"""