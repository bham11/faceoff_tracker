import pandas as pd
import sqlalchemy
from pandas.io import sql
from jinja2 import *
import os


ZONE_MAPPING = {
    "1": "RO",
    "2": "LO",
    "3": "RONZ",
    "4": "LONZ",
    "5": "C",
    "6": "LDNZ",
    "7": "RDNZ",
    "8": "LD",
    "9": "RD",
}


ZONE_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

ROOT = "/Users/brandonhampstead/Documents/NortheasternHockey/faceoff_tracker/src"
DB_TEMP_PATH = f"{ROOT}/utils/faceoff_data_model.csv"
PATH_TO_DESKTOP = "/Users/brandonhampstead/Desktop/"


class HockeyDatabase:
    def __init__(self, columns_file) -> None:
        self.database_columns_csv = pd.read_csv(columns_file, index_col=False)

        # db engine
        self.engine = sqlalchemy.create_engine("sqlite:///:memory:")

        # storing dataframe in a table
        self.hockey_faceoff_data_table = self.database_columns_csv.to_sql(
            "hockey_faceoff_data_table", self.engine, index=False
        )

        # variable to save a possible stats dataframe to export to excel
        self.df_to_export = pd.DataFrame()

    def add_filter_to_list(self, filter_list, filter):
        if len(filter_list) == 0:
            filter_list = filter_list + filter
        else:
            filter_list = filter_list + " AND " + filter
        return filter_list

    def build_hockey_query_db(
        self, table_name, husky: str, opp: str, period: str, strength: str, zone: str
    ):
        filter_list = []
        query = f"Select * From {table_name}"
        filters = ""
        if husky != "":
            filters = self.add_filter_to_list(filters, f"Player= {husky}")
            filter_list.append(f"Player= {husky}")
        if opp != "":
            filters = self.add_filter_to_list(filters, f"Opponent= {opp}")
            filter_list.append(f"Opponent= {opp}")
        if zone != "":
            # group_bys = group_bys + ", Zone"
            filters = self.add_filter_to_list(filters, f"Zone= '{zone}'")
            filter_list.append(f"Zone= '{zone}'")
        if period != "all per":
            filters = self.add_filter_to_list(filters, f"Period= '{period}'")
            filter_list.append(f"Period= '{period}'")
        if strength != "all str":
            filters = self.add_filter_to_list(filters, f"Strength= '{strength}'")
            filter_list.append(f"Strength= '{strength}'")
        # adding table to end of query
        if len(filters) > 0:
            query = "{0} WHERE {1}".format(query, filters)
        environment = Environment(loader=FileSystemLoader("sql_templates/"))
        template = environment.get_template("hockey_db_query.sql")
        sql = template.render(table_name=table_name, filters=filter_list)
        return sql

    def build_hockey_query(
        self,
        table_name,
        husky: str,
        opp: str,
        period: str,
        strength: str,
        zone: str,
        by_opp: str,
    ):
        query = "Select Player"
        fo_percetnage_query = (
            ', CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || '
            'CAST(count(result) AS varchar) AS "FO%"'
        )
        group_bys = " GROUP BY Player"
        table = f" FROM {table_name}"
        filters = ""
        if husky != "":
            filters = self.add_filter_to_list(filters, f"Player= {husky}")
        if opp != "":
            query = query + ", Opponent"
            filters = self.add_filter_to_list(filters, f"Opponent= {opp}")
        if zone != "":
            group_bys = group_bys + ", Zone"
            query = query + ", Zone"
            filters = self.add_filter_to_list(filters, f"Zone= '{zone}'")
        if period != "all per":
            filters = self.add_filter_to_list(filters, f"Period= '{period}'")
        if strength != "all str":
            filters = self.add_filter_to_list(filters, f"Strength= '{strength}'")
        if by_opp != "not op groups":
            query = query + ", Opponent"
            group_bys = group_bys + ", Opponent"
        # adding table to end of query
        query = query + fo_percetnage_query + table
        if len(filters) > 0:
            query = "{0} WHERE {1}".format(query, filters)
        return query + group_bys

    def return_query_df(self, query):
        return pd.read_sql_query(query, self.engine)

    def insert_faceoff(self, period, husky, opp, strength, zone, result):
        sql.execute(
            "INSERT INTO hockey_faceoff_data_table VALUES(?,?,?,?,?,?)",
            self.engine,
            params=[(period, husky, opp, strength, zone, result)],
        )

    def save_df_to_csv(self, df, path):
        df.to_csv(os.path.join(PATH_TO_DESKTOP, f"{path}.csv"), index=False)
