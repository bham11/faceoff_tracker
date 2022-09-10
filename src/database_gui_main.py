import tkinter as tk
from tkinter import END, BOTTOM, NONE

import pandas as pd
import sqlalchemy
from pandas.io import sql
from sqlalchemy import select, column

from src.faceoff_data import ZONE_MAPPING, HUSKIES
from PIL import ImageTk, Image

if __name__ == '__main__':

    # creating a database instance
    database_columns_csv = pd.read_csv('faceoff_data_model.csv', index_col=False)

    # db engine
    engine = sqlalchemy.create_engine('sqlite:///:memory:')

    # storing dataframe in a table
    hockey_faceoff_data_table = database_columns_csv.to_sql('hockey_faceoff_data_table', engine, index=False)
    fields = "Period,Player,Opponent,Strength,Zone,Result"
    # res1 = pd.read_sql_query(f'SELECT * FROM hockey_faceoff_data_table', engine)

    window = tk.Tk()
    window.title("Northeastern Huskies Hockey - Faceoff Tracker")
    # Full screen
    # window.state("zoomed")

    # frame of the input boxs, labels and log
    input_frame = tk.LabelFrame(text='Inputs:')

    what_zone = tk.Label(master=input_frame, text="What Zone (1-9)?")
    zone = tk.Entry(master=input_frame, width=2)

    what_husky = tk.Label(master=input_frame, text="What Husky?")
    husky = tk.Entry(master=input_frame,width=2 )

    what_opp = tk.Label(master=input_frame, text="What Opp?")
    opp = tk.Entry(master=input_frame,width=2 )

    ask_result = tk.Label(master=input_frame, text="Result (W/L)?")
    result = tk.Entry(master=input_frame,width=2 )

    # period and strength frame
    per_str_frame = tk.LabelFrame(text='Options')


    # period radio buttons, will send that period to the add_FO method upon the enter of the result
    what_period = tk.StringVar(value="1rst")
    first_period = tk.Radiobutton(master=per_str_frame, text="1rst", value="1rst", variable=what_period)
    second_period = tk.Radiobutton(master=per_str_frame, text="2nd", value="2nd", variable=what_period)
    third_period = tk.Radiobutton(master=per_str_frame, text="3rd", value="3rd", variable=what_period)
    ot = tk.Radiobutton(master=per_str_frame, text="OT", value="OT", variable=what_period)

    # strength radio buttons, will send that strength to the add_Fo method upon enter of the result
    strength = tk.StringVar(value="even")
    even = tk.Radiobutton(master=per_str_frame, text="Even", value="even", variable=strength)
    pk = tk.Radiobutton(master=per_str_frame, text="PK", value="pk", variable=strength)
    pp = tk.Radiobutton(master=per_str_frame, text="PP", value="pp", variable=strength)


    def clear_ents():
        zone.delete(0, END)
        husky.delete(0, END)
        opp.delete(0, END)
        result.delete(0, END)
        zone.focus()


    clear_entries = tk.Button(master=input_frame, text="Clear", command=clear_ents)

    log = tk.Text(master=input_frame,width=40)

    # packing input widgets and frame
    first_period.grid(row=0,column=1)
    second_period.grid(row=0,column=3)
    third_period.grid(row=0,column=5)
    ot.grid(row=0,column=7)
    even.grid(row=1,column=2)
    pp.grid(row=1,column=4)
    pk.grid(row=1,column=6)
    what_zone.grid(row=2,column=3)
    zone.grid(row=2,column=4)
    what_husky.grid(row=3,column=3)
    husky.grid(row=3,column=4)
    what_opp.grid(row=4,column=3)
    opp.grid(row=4,column=4)
    ask_result.grid(row=5,column=3)
    result.grid(row=5,column=4)
    clear_entries.grid(row=6,column=4)
    log.grid(row=7,column=4)



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


    # stats frame and widgets
    stats_frame = tk.Frame()
    slog_scrollbar = tk.Scrollbar(stats_frame, orient="horizontal")
    stats_log = tk.Text(master=stats_frame, wrap=NONE, xscrollcommand=slog_scrollbar.set)
    whose_stats = tk.Label(master=stats_frame, text="What Husky's FO stats?")
    look_up = tk.Entry(master=stats_frame)


    def display_stats():
        pass


    def display_percentage():
        wins = 'SELECT  count(result) FROM hockey_faceoff_data_table WHERE result="w"  ' \
               'GROUP BY Player,zone'
        totals = 'SELECT count(result) FROM hockey_faceoff_data_table GROUP BY Player,zone '


        query = f'SELECT ({wins}) / ({totals}) FROM hockey_faceoff_data_table GROUP BY Player,zone'
        print(pd.read_sql_query(wins, engine))


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

    # packing frames
    per_str_frame.pack(side='top', ipady=10)
    rink_frame.pack(side='left', fill='both')
    input_frame.pack(side='left', fill='both')
    stats_frame.pack(side='left',fill='both')


    # focusing on inputs
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


    index = 0


    def add_FO(e):
        # use csv as rdb to add this faceoff as a single entry with
        # period, player, opp, str, zone(mapped), result

        formatted_zone = ZONE_MAPPING[zone.get()]
        sql.execute('INSERT INTO hockey_faceoff_data_table VALUES(?,?,?,?,?,?)', engine,
                    params=[(what_period.get(), husky.get(), opp.get(), strength.get(), formatted_zone, result.get())])
        # print(pd.read_sql_query(f'SELECT * FROM hockey_faceoff_data_table', engine))
        # query = 'SELECT  player, count(result) AS "wins", zone FROM hockey_faceoff_data_table
        # WHERE result="w"  GROUP BY Player, Zone '
        # print(pd.read_sql_query(query, engine))

        log.insert("1.0", f"{husky.get()} vs {opp.get()} in zone {formatted_zone}: {result.get()}\n")

        clear_ents()


    zone.bind("<Return>", valid_zone)
    husky.bind("<Return>", valid_husky)
    opp.bind("<Return>", valid_opp)
    result.bind("<Return>", add_FO)

    window.mainloop()
