# Euroleague Wiki
A 2024-25 term project by the group Cyclones for the BLG317E Database Systems course given in ITU.

## Project Description
The project aims to offer a website where people can find valuable information regarding the history of Euroleague, including all of the teams, matches and the details of every point scored in those matches to name a few. Euroleague Wiki also features user authentication and authorization, allowing admins to create/view/update/delete entries or users from the website and the database. Ranging from the 2007-08 season to 2024-25, the website contains Euroleague data of the last 17 years by utilizing a public dataset.

The public dataset that will be partially used for the project: [Kaggle - Euroleague Datasets](https://www.kaggle.com/datasets/babissamothrakis/euroleague-datasets "Kaggle - Euroleague Datasets")

## Tech Stack
### Backend
- **Programming Language:** Python
- **Framework:** Flask
- **Database:** MySQL
- **External Libraries:** Bcrypt (Password encryption)
### Frontend
- **Markup Language:** HTML
- **Styling:** CSS, Bootstrap
- **Scripting:** JavaScript

## Prerequisites
The project makes use of Flask, Python MySQL Connector and Bcrypt. Please make sure to create a virtual environment and install the necessary requirements by running these commands on a terminal after Step 7 in the [Installation Guide](#installation-guide) section:
```
# UNIX
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```
# WINDOWS
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
You should also have Python3, MySQL and preferably MySQL Workbench installed on your system.

## Installation Guide
For the full installation, go through these steps one by one:

1. Open MySQL and run the following command in order to find your MySQL secure file directory.
```
SHOW VARIABLES LIKE "secure_file_priv"
```

2. Download all the related .csv files from [Euroleague Wiki - Google Drive](https://drive.google.com/drive/folders/1zTKZ5-p6dJxQMiqAzx1hXLQBIRJp8dwe?usp=drive_link "Euroleague Wiki - Google Drive") and copy them into the directory you have found in the first step.

3. From the /db/database_final folder on github, download the create_db_final.sql file, and in the "load data infile" parts, change the default directory given to your secure file directory.
```
{D:/ProgramData/MySQL/MySQL Server 8.0/Uploads/} -> CTRL + F REPLACE ALL
```

4. If you're using MySQL Workbench, go to Edit -> Preferences -> SQL Editor -> MySQL Session. Increase all of the intervals, preferably to 800 seconds so that the huge amount of data from the CSV files can load into the tables successfully without getting timed out.

5. Execute the create_db_final.sql file in MySQL.

6. Go to a local directory of your preference and clone the github project by running the following command.
```
git clone https://github.com/g-akca/euroleague-wiki.git
```

7. Create a virtual environment and install the project dependencies by using the commands in the [Prerequisites](#prerequisites) section. After that, run server.py with the commands below.
```
# UNIX
.venv/bin/python3 server.py
```
```
# WINDOWS
.venv\Scripts\python server.py
```

8. You can browse the website now.

## Acknowledgements
- [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/ "Bootstrap")
