import pandas as pd
import sqlalchemy

ONE_DRIVE_PATH = "/Users/brandonhampstead/Library/CloudStorage/OneDrive-NortheasternUniversity" \
                 "/Hockey Ops/2022-23 Season/2022-2023 FO Stats/"
OPPONENT_GAME_LOG = "LIU/Game 1/vsLIU_log.csv"

PATH_TO_DESKTOP = '/Users/brandonhampstead/Desktop/'

FULL_DB_PATH = ONE_DRIVE_PATH + OPPONENT_GAME_LOG

database_columns_csv = pd.read_csv(
    FULL_DB_PATH,
    index_col=False)
# db engine
engine = sqlalchemy.create_engine('sqlite:///:memory:')

# storing dataframe in a table
hockey_faceoff_data_table = database_columns_csv.to_sql('hockey_faceoff_data_table', engine, index=False)

wins_div_loss = 'CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || ' \
                f'CAST(count(result) AS varchar) AS "FO%"'

freestyle_query = f'SELECT Player,{wins_div_loss} FROM hockey_faceoff_data_table GROUP BY Player'

totals_query = f'SELECT Player,{wins_div_loss} FROM hockey_faceoff_data_table GROUP BY Player'

player_by_zone_query = f'SELECT Player, Zone, {wins_div_loss} FROM hockey_faceoff_data_table GROUP BY Player, Zone'

player_by_opp_query = f'SELECT Player, Opponent, {wins_div_loss} FROM hockey_faceoff_data_table GROUP BY Player, Opponent'

team_tots_by_zone_query = f'SELECT Zone, {wins_div_loss} FROM hockey_faceoff_data_table GROUP BY Zone'

# tables for queries
tots_by_player_table = pd.read_sql_query(totals_query, engine)

player_by_zone_table = pd.read_sql_query(player_by_zone_query, engine)

player_by_opp_table = pd.read_sql_query(player_by_opp_query, engine)

tots_by_zone_table = pd.read_sql_query(team_tots_by_zone_query, engine)

freestyle_table = pd.read_sql_query(freestyle_query, engine)

csv_name = "totals_by_player"

if __name__ == '__main__':
    tots_by_player_table.to_csv(f'{PATH_TO_DESKTOP}totals_by_player.csv', index=False)
    player_by_zone_table.to_csv(f'{PATH_TO_DESKTOP}player_by_zone.csv', index=False)
    player_by_opp_table.to_csv(f'{PATH_TO_DESKTOP}player_by_opp.csv', index=False)
    tots_by_zone_table.to_csv(f'{PATH_TO_DESKTOP}team_tots_by_zone.csv', index=False)
    print('Completed compiling files on desktop. Go Huskies!')
