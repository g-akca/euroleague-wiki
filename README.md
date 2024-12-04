# Euroleague Wiki
A 2024-25 term project by the group Cyclones for the BLG317E Database Systems course given in ITU.

The project aims to offer a website where people can find valuable information regarding the history of Euroleague, including all of the teams, matches and the details of every point scored in those matches to name a few. Ranging from the 2007-08 season to 2024-25, the website contains Euroleague data of the last 17 years by utilizing a public dataset.

The public dataset that will be partially used for the project: https://www.kaggle.com/datasets/babissamothrakis/euroleague-datasets

====Installation Guide====
0. Requirements - Python3, MySQL, MySQL Workbench (Preferred - Not Necessary)
1. Open your preferred IDE, download flask and mysql.connector
-- pip install Flask, pip install mysql-connector-python
2. Open MySQL, run the following command in order to find the usable folder location.
-- SHOW VARIABLES LIKE "secure_file_priv"
3. Copy all the .csv files into the given directory.
-- https://drive.google.com/drive/folders/1zTKZ5-p6dJxQMiqAzx1hXLQBIRJp8dwe?usp=drive_link
4. From /db/database_final get the create_db_final.sql file, in the load data part, change the directory to your secure file directory.
-- {D:/ProgramData/MySQL/MySQL Server 8.0/Uploads/} -> CTRL + F REPLACE ALL
5. From the given path, increase the intervals, preferably to 200 seconds.
-- Edit -> Preferences -> SQL Editor -> MySQL Session
6. Execute create_db_final.sql in MySQL
7. Back to the IDE, run server.py.
-- If connection cannot be established, change the password and user in the db.py to match with your system.
