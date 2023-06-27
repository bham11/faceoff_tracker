from gui import *
from hockey_db import *

ROOT = '/Users/brandonhampstead/Documents/NortheasternHockey/faceoff_tracker/src'
DB_TEMP_PATH = f'{ROOT}/utils/faceoff_data_model.csv'

if __name__ == '__main__':
    database = HockeyDatabase(DB_TEMP_PATH)
    window = HockeyWindow(database)
    window.mainloop()