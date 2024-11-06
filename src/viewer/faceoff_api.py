import sqlite3
import pandas as pd
import re

class FaceoffAPI:
    con = None

    @staticmethod
    def connect(dbfile):
        """make a connection"""
        FaceoffAPI.con = sqlite3.connect("dbfile", check_same_thread=False)

    @staticmethod
    def load_table(file_path: str):
        df = pd.read_csv(file_path)
        table_name = file_path.split("/")[-1].split("log")[0]
        cleaned_table_name = table_name[:len(table_name)-1]
        with FaceoffAPI.con as conn:
            df.to_sql(cleaned_table_name, conn, if_exists='replace', index=False)
            conn.commit()
        return "Table committed"
        

    @staticmethod
    def execute(query):
        return pd.read_sql_query(query, FaceoffAPI.con)

    @staticmethod
    def get_faceoff_splits(table):
        query = f'SELECT CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || CAST(count(result) AS varchar) AS "FO%" from {table}'
        df = FaceoffAPI.execute(query)
        return list(df)


if __name__ == "__main__":
    api = FaceoffAPI()
    print(api.load_table("test.csv"))
