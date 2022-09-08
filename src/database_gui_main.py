import tkinter as tk
from tkinter import END, BOTTOM, NONE

import pandas as pd
import sqlalchemy

from src.faceoff_data import ZONE_MAPPING, HUSKIES
from PIL import ImageTk, Image

if __name__ == '__main__':

    # creating a database instance
    database_columns_csv = pd.read_csv('faceoff_data_model.csv', index_col=False)
    database_columns_csv = database_columns_csv.reset_index(drop=True)

    # db engine
    engine = sqlalchemy.create_engine('sqlite:///:memory:')

    # storing dataframe in a table
    database_columns_csv.to_sql('hockey_faceoff_data_table', engine)
    fields = "Period,Player,Opponent,Strength,Zone,Result"
    res1 = pd.read_sql_query(f'SELECT {fields} FROM hockey_faceoff_data_table', engine)
    print(res1)

    window = tk.Tk()
    window.title("Northeastern Huskies Hockey - Faceoff Tracker")
    # Full screen
    # window.state("zoomed")

    input_frame = tk.Frame()

    what_zone = tk.Label(master=input_frame, text="What Zone (1-9)?")
    zone = tk.Entry(master=input_frame, )

    what_husky = tk.Label(master=input_frame, text="What Husky?")
    husky = tk.Entry(master=input_frame, )

    what_opp = tk.Label(master=input_frame, text="What Opp?")
    opp = tk.Entry(master=input_frame, )

    ask_result = tk.Label(master=input_frame, text="Result (W/L)?")
    result = tk.Entry(master=input_frame, )


    def clear_ents():
        zone.delete(0, END)
        husky.delete(0, END)
        opp.delete(0, END)
        result.delete(0, END)
        zone.focus()


    clear_entries = tk.Button(master=input_frame, text="Clear", command=clear_ents)

    log = tk.Text(master=input_frame)

    # packing input widgets and frame
    what_zone.pack()
    zone.pack()
    what_husky.pack()
    husky.pack()
    what_opp.pack()
    opp.pack()
    ask_result.pack()
    result.pack()
    clear_entries.pack()
    log.pack()

    input_frame.pack(side="right")

    # rink photo for zone clues
    rink_frame = tk.Frame()
    photo = Image.open("hori_hockey_rink.png")
    re_sized_photo = photo.resize((500, 200))
    hockey_rink = ImageTk.PhotoImage(re_sized_photo)
    rink_photo = tk.Label(master=rink_frame, image=hockey_rink)

    sec_photo = Image.open("second_period_rink.png").resize((500, 200))
    second_rink = ImageTk.PhotoImage(sec_photo)

    second_rink_photo = tk.Label(master=rink_frame, image=second_rink)

    rink_photo.pack()
    second_rink_photo.pack()
    rink_frame.pack(side="top")

    # stats frame and widgets
    stats_frame = tk.Frame()
    slog_scrollbar = tk.Scrollbar(stats_frame, orient="horizontal")
    stats_log = tk.Text(master=stats_frame, wrap=NONE, xscrollcommand=slog_scrollbar.set)
    whose_stats = tk.Label(master=stats_frame, text="What Husky's FO stats?")
    look_up = tk.Entry(master=stats_frame)


    def display_stats():
        pass


    def display_percentage():
        pass


    # look_up.bind("<Enter>", display_stats)
    display_bttn = tk.Button(master=stats_frame, text="Search", command=display_stats)
    whose_percentage = tk.Button(master=stats_frame, text="FO %", command=display_percentage)

    whose_stats.pack()
    look_up.pack()
    display_bttn.pack()
    whose_percentage.pack()
    stats_log.pack()
    slog_scrollbar.pack(side=BOTTOM, fill='x')
    slog_scrollbar.config(command=stats_log.xview)
    stats_frame.pack(side="left")

    zone.focus()


    def valid_zone(e):
        zone_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if zone.get() not in zone_list:
            log.insert("1.0", "Please input a valid zone: 1-9\n")
            zone.delete(0, END)
            zone.focus()
        else:
            husky.focus()


    def valid_husky(e):
        center_list = ['10', '27', '29', '7', '15']
        if not husky.get().isdigit():
            log.insert("1.0", "Please input a valid husky jersey\n")
            husky.delete(0, END)
            husky.focus()
        else:
            opp.focus()


    def valid_opp(e):
        if not opp.get().isdigit():
            log.insert("1.0", "Please input a valid opponent jersey number\n")
            opp.delete(0, END)
            opp.focus()
        else:
            result.focus()


    def add_FO(e):
        # use csv as rdb to add this faceoff as a single entry with
        # period, player, opp, str, zone(mapped), result

        formatted_zone = ZONE_MAPPING[zone.get()]

        log.insert("1.0", f"{husky.get()} vs {opp.get()} in zone {formatted_zone}: {result.get()}\n")

        clear_ents()


    zone.bind("<Return>", valid_zone)
    husky.bind("<Return>", valid_husky)
    opp.bind("<Return>", valid_opp)
    result.bind("<Return>", add_FO)

    window.mainloop()
