import tkinter as tk
from tkinter import *

import pandas as pd
import sqlalchemy
from pandas.io import sql
from sqlalchemy import select, column

from src.faceoff_data import ZONE_MAPPING
from PIL import ImageTk, Image


def build_hockey_query(table_name, husky=None, opp=None, period=None, strength=None, zone=None):
    # f'SELECT Player, zone, CAST(count(result) FILTER(WHERE result = "w" and period = "{per}" ) AS varchar) || "/" || ' \
    # f'CAST(count(result) FILTER(WHERE period = "{per}" ) AS varchar) AS "FO%" FROM hockey_faceoff_data_table GROUP BY Player,zone'
    query = 'Select * FROM hockey_faceoff_data_table'
    if period is not None:
        if husky is None:
            query = f'SELECT Player, zone, CAST(count(result) FILTER(WHERE result = "w" and period = "{period}" ) AS varchar) ' \
                    f'|| "/" || CAST(count(result) FILTER(WHERE period = "{period}" ) ' \
                    f'AS varchar) AS "FO%" FROM hockey_faceoff_data_table GROUP BY Player,zone'

    return query


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
    input_frame.config(width=200)

    what_zone = tk.Label(master=input_frame, text="What Zone (1-9)?")
    zone = tk.Entry(master=input_frame, width=2)

    what_husky = tk.Label(master=input_frame, text="What Husky?")
    husky = tk.Entry(master=input_frame, width=2)

    what_opp = tk.Label(master=input_frame, text="What Opp?")
    opp = tk.Entry(master=input_frame, width=2)

    ask_result = tk.Label(master=input_frame, text="Result (W/L)?")
    result = tk.Entry(master=input_frame, width=2)

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

    log = tk.Text(master=input_frame, width=40)

    # packing options widgets
    first_period.grid(row=0, column=1)
    second_period.grid(row=0, column=3)
    third_period.grid(row=0, column=5)
    ot.grid(row=0, column=7)
    even.grid(row=1, column=2)
    pp.grid(row=1, column=4)
    pk.grid(row=1, column=6)

    # packing input widgets
    what_zone.grid(row=1, column=1)
    zone.grid(row=1, column=2)
    what_husky.grid(row=2, column=1)
    husky.grid(row=2, column=2)
    what_opp.grid(row=3, column=1)
    opp.grid(row=3, column=2)
    ask_result.grid(row=4, column=1)
    result.grid(row=4, column=2)
    clear_entries.grid(row=5, column=2)
    log.grid(row=6, columnspan=5)

    # rink photo for zone clues
    rink_frame = tk.LabelFrame(text="Rink Mappings")
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
    stats_frame = tk.LabelFrame(text="Display Stats", )
    slog_scrollbar = tk.Scrollbar(stats_frame, orient="horizontal")
    stats_log = tk.Text(master=stats_frame, wrap=NONE, xscrollcommand=slog_scrollbar.set)
    whose_stats = tk.Label(master=stats_frame, text="What Husky's FO stats?")
    what_opp = tk.Label(master=stats_frame, text="Against Who?")
    look_up = tk.Entry(master=stats_frame, width=2)
    opp_look_up = tk.Entry(master=stats_frame, width=2)

    # options buttons for stat tracking
    filter_periods = tk.StringVar(value="all per")
    filter_first_period = tk.Radiobutton(master=stats_frame, text="1rst", value="1rst", variable=filter_periods)
    filter_second_period = tk.Radiobutton(master=stats_frame, text="2nd", value="2nd", variable=filter_periods)
    filter_third_period = tk.Radiobutton(master=stats_frame, text="3rd", value="3rd", variable=filter_periods)
    filter_ot = tk.Radiobutton(master=stats_frame, text="OT", value="OT", variable=filter_periods)
    filter_all_periods = tk.Radiobutton(master=stats_frame, text="All Per", value="all per", variable=filter_periods)

    filter_strength = tk.StringVar(value="all str")
    filter_even = tk.Radiobutton(master=stats_frame, text="Even", value="even", variable=filter_strength)
    filter_pk = tk.Radiobutton(master=stats_frame, text="PK", value="pk", variable=filter_strength)
    filter_pp = tk.Radiobutton(master=stats_frame, text="PP", value="pp", variable=filter_strength)
    filter_all_strengths = tk.Radiobutton(master=stats_frame, text="All Strs", value="all str",
                                          variable=filter_strength)


    def display_stats():
        pass


    def display_percentage():
        per = filter_periods.get()
        husky = look_up.get()
        opp = opp_look_up.get() # def mapInput(....get()) -> turns '' to none, validates input and returns valid inputs
        # def build_hockey_query(table_name, husky=None,opp=None, period=None, strength=None)
        if per != "all per" and husky == "":
            q2 = build_hockey_query(table_name='hockey_faceoff_data_table',period=per)
        else:

            q2 = 'SELECT Player, zone, CAST(count(result) FILTER(WHERE result = "w") AS varchar) || "/" || ' \
                 'CAST(count(result) AS varchar) AS "FO%" FROM hockey_faceoff_data_table GROUP BY Player,zone'
        stats_log.delete("1.0", END)
        stats_log.insert("1.0", pd.read_sql_query(q2, engine).to_markdown(index=False))


    display_bttn = tk.Button(master=stats_frame, text="Search", command=display_stats)
    whose_percentage = tk.Button(master=stats_frame, text="FO %", command=display_percentage)

    # option buttons on stat frame packing
    filter_all_periods.grid(row=0, column=0)
    filter_first_period.grid(row=0, column=1)
    filter_second_period.grid(row=0, column=2)
    filter_third_period.grid(row=0, column=3)
    filter_ot.grid(row=0, column=4)

    filter_all_strengths.grid(row=3, column=0)
    filter_even.grid(row=3, column=1)
    filter_pp.grid(row=3, column=2)
    filter_pk.grid(row=3, column=3)

    whose_stats.grid(row=4, column=0)
    look_up.grid(row=4, column=1)
    what_opp.grid(row=5, column=0)
    opp_look_up.grid(row=5, column=1)
    display_bttn.grid(row=6, column=1)
    whose_percentage.grid(row=7, column=1)
    stats_log.grid(row=8, columnspan=5)
    slog_scrollbar.grid(row=9, columnspan=5)
    slog_scrollbar.config(command=stats_log.xview)

    # packing frames
    per_str_frame.pack(side='top', ipady=10)
    rink_frame.pack(side='left', fill='both')
    input_frame.pack(side='left', fill='both')
    stats_frame.pack(side='left', fill='both')

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

        period_map = {
            "1rst": "P1",
            "2nd": "P2",
            "3rd": "P3",
            "OT": "OT"
        }
        formatted_period = period_map[what_period.get()]
        formatted_zone = ZONE_MAPPING[zone.get()]
        sql.execute('INSERT INTO hockey_faceoff_data_table VALUES(?,?,?,?,?,?)', engine,
                    params=[(what_period.get(), husky.get(), opp.get(), strength.get(),
                             formatted_zone, result.get().lower())])
        # print(pd.read_sql_query(f'SELECT * FROM hockey_faceoff_data_table', engine))
        # query = 'SELECT  player, count(result) AS "wins", zone FROM hockey_faceoff_data_table
        # WHERE result="w"  GROUP BY Player, Zone '
        # print(pd.read_sql_query(query, engine))

        log.insert("1.0",
                   f"{formatted_period}: {husky.get()} vs {opp.get()} in zone {formatted_zone}: {result.get()}\n")

        clear_ents()


    zone.bind("<Return>", valid_zone)
    husky.bind("<Return>", valid_husky)
    opp.bind("<Return>", valid_opp)
    result.bind("<Return>", add_FO)

    window.mainloop()
