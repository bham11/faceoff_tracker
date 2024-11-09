import duckdb 
import pandas as pd


class FaceoffAPI:
    
    def __init__(self, csv_file_path):
        """
        Initializes the Faceoff object by loading the CSV file into a pandas DataFrame.
        
        :param csv_file_path: Path to the CSV file.
        """
        self.csv_file_path = csv_file_path
        self.table_name = "test"
        self.df = self.load_csv()
        self.con = duckdb.connect()  # Initialize DuckDB connection
        self.register_dataframe("test")
        
    def load_csv(self):
        try:
            df = pd.read_csv(self.csv_file_path)
            print(f"CSV file '{self.csv_file_path}' loaded successfully.")
            return df
        except Exception as e:
            raise ValueError(f"Failed to load CSV file: {e}")
        
    def register_dataframe(self, table_name):
        """
        Registers the pandas DataFrame as a table in DuckDB.
        """
        self.con.register(f"{table_name}", self.df)
        print("DataFrame registered as f'{data_table}' in DuckDB.")
        
    
    def extract_table_name(self):
        table_name =self.csv_file_path.split("/")[-1].split("log")[0]
        cleaned_table_name = table_name[:len(table_name)-1]
        return cleaned_table_name
        

    def execute_query(self, query):
        """
        Executes a SQL query on the registered DataFrame in DuckDB.
        
        :param query: SQL query string to execute.
        :return: Query results as a list of dictionaries.
        """
        try:
            return self.con.sql(query).df()
        except Exception as e:
            raise ValueError(f"Failed to execute query: {e}")

    def get_faceoff_splits(self):
        query = f'SELECT CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || CAST(count(result) AS varchar) AS "FO%" from {self.table_name}'
        query = f"SELECT * FROM {self.table_name}"
        df = self.execute_query(query)
        return df


if __name__ == "__main__":
    api = FaceoffAPI("/Users/brandonhampstead/Library/CloudStorage/OneDrive-NortheasternUniversity/Hockey Ops/2023-24 Season/2023-2024 FO Stats/Game Logs/03_16_2024_vs_BU_log_output.csv")
    print(api.get_faceoff_splits())
