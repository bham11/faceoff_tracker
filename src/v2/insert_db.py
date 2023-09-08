import sqlite3
from jinja2 import *
import pandas as pd
import os

ROOT = '/Users/brandonhampstead/Documents/NortheasternHockey/faceoff_tracker/src'
DB_TEMP_PATH = f'{ROOT}/utils/faceoff_data_model.csv'
PATH_TO_DESKTOP = '/Users/brandonhampstead/Desktop/'


OPPONENTS = [
    "Stonehill",
    "Quinnipiac",
    "Bentley",
    "UNH",
    "Merrimack",
    "UMass",
    "Providence",
    "RPI",
    "BC",
    "Brown",
    "BU",
    "UVM",
    "Maine",
    "Harvard",
    "UML",
    "UConn",
]

def render_jinja(template, **args):
    environment = Environment(loader=FileSystemLoader("sql_templates/"))
    template = environment.get_template(template)
    sql = template.render(**args)
    return sql

def create_table(opponent):
    args = {"opponent": opponent}
    sql = render_jinja("create_opp_table.sql", **args)
    return sql
def insert_row(team):
    args = {"team": team}
    sql = render_jinja("insert_into_db.sql", **args)
    return sql

def execute_db_creation(database):
    connection = sqlite3.connect(database)
    c = connection.cursor()
    
    for team in OPPONENTS:
        c.execute(create_table(team))
    
    connection.commit()
    connection.close()

def insert_game(database,team, csv_path):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    game_data = pd.read_csv(csv_path)
    
    for row in game_data.itertuples():
        c.execute(insert_row(team), 
                  (row.Period, 
                   row.Player, 
                   row.Opponent, 
                   row.Strength, 
                   row.Zone, 
                   row.Result))
    
    conn.commit()
    conn.close()

def select_opponent_data(database, team, breakdown):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    
    statement = f"SELECT Period, Player, Opponent, Strength, Zone, Result FROM {team}"
    
    c.execute(statement)
    
    rows = c.fetchall()
    
    columns = ['Period', 'Husky', 'Opp', 'Strength', 'Zone', 'Result']
    return pd.DataFrame(rows, columns=columns, index=None)

        
    
    
    

if __name__ == '__main__':
    # execute_db_creation("2023-2024/hockey.db")
    # insert_game("2023-2024/hockey.db", "BU", os.path.join(PATH_TO_DESKTOP, "log_output.csv"))
    
    select_opponent_data("2023-2024/hockey.db", "BU", "sus")
    