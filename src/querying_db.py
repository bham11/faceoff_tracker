import pandas as pd
import sqlalchemy

DB_PATH = "/Users/brandonhampstead/Library/CloudStorage/OneDrive-NortheasternUniversity" \
          "/Hockey Ops/2022-23 Season/2022-2023 FO Stats/LIU/Game 1/vsLIU_log.csv"

PATH_TO_DESKTOP ='/Users/brandonhampstead/Desktop/'

database_columns_csv = pd.read_csv(
        DB_PATH,
        index_col=False)
# db engine
engine = sqlalchemy.create_engine('sqlite:///:memory:')

# storing dataframe in a table
hockey_faceoff_data_table = database_columns_csv.to_sql('hockey_faceoff_data_table', engine, index=False)

wins_div_loss = 'CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || ' \
                          f'CAST(count(result) AS varchar) AS "FO%"'

query = f'SELECT Player, Zone, {wins_div_loss} FROM hockey_faceoff_data_table GROUP BY Player, Zone'


display_table = pd.read_sql_query(query, engine)
csv_name = "test_query"
display_table.to_csv(f'{PATH_TO_DESKTOP}{csv_name}.csv',index=False)

if __name__ == '__main__':
    display_table.to_csv(f'{PATH_TO_DESKTOP}{csv_name}.csv', index=False)