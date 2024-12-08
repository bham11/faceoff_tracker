from gui import HockeyWindow
from hockey_db import HockeyDatabase

ROOT = "/Users/brandonhampstead/Documents/NortheasternHockey/faceoff_tracker/src"
DB_TEMP_PATH = f"{ROOT}/utils/faceoff_data_model.csv"
PATH_TO_DESKTOP = "/Users/brandonhampstead/Desktop/"

if __name__ == "__main__":
    database = HockeyDatabase(DB_TEMP_PATH)
    window = HockeyWindow(database)
    window.mainloop()
