from gui import HockeyWindow
from hockey_db import HockeyDatabase
from constants import DB_TEMP_PATH

if __name__ == "__main__":
    database = HockeyDatabase(DB_TEMP_PATH)
    window = HockeyWindow(database)
    window.mainloop()
