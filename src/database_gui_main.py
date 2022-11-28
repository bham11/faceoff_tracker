import tkinter as tk
from tkinter import *

import pandas as pd
import sqlalchemy
import tkinter.scrolledtext as tkscrolled
from pandas.io import sql

from PIL import ImageTk, Image

ZONE_MAPPING = {
    "1": "RO",
    "2": "LO",
    "3": "RONZ",
    "4": "LONZ",
    "5": "C",
    "6": "LDNZ",
    "7": "RDNZ",
    "8": "LD",
    "9": "RD"

}

ZONE_LIST = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def add_filter_to_list(filter_list, filter):
    if len(filter_list) == 0:
        filter_list = filter_list + filter
    else:
        filter_list = filter_list + " AND " + filter
    return filter_list


def build_hockey_query_db(table_name, husky: str, opp: str, period: str, strength: str, zone: str):
    query = f'Select * From {table_name}'
    filters = ''
    if husky != "":
        filters = add_filter_to_list(filters, f"Player= {husky}")
    if opp != "":
        filters = add_filter_to_list(filters, f"Opponent= {opp}")
    if zone != "":
        # group_bys = group_bys + ", Zone"
        filters = add_filter_to_list(filters, f"Zone= '{zone}'")
    if period != "all per":
        filters = add_filter_to_list(filters, f"Period= '{period}'")
    if strength != "all str":
        filters = add_filter_to_list(filters, f"Strength= '{strength}'")
    # adding table to end of query
    if len(filters) > 0:
        query = "{0} WHERE {1}".format(query, filters)
    return query


def build_hockey_query(table_name, husky: str, opp: str, period: str, strength: str, zone: str, by_opp: str):
    query = 'Select Player'
    fo_percetnage_query = ', CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || ' \
                          f'CAST(count(result) AS varchar) AS "FO%"'
    group_bys = " GROUP BY Player"
    table = f" FROM {table_name}"
    filters = ''
    if husky != "":
        filters = add_filter_to_list(filters, f"Player= {husky}")
    if opp != "":
        query = query + ", Opponent"
        filters = add_filter_to_list(filters, f"Opponent= {opp}")
    if zone != "":
        group_bys = group_bys + ", Zone"
        query = query + ", Zone"
        filters = add_filter_to_list(filters, f"Zone= '{zone}'")
    if period != "all per":
        filters = add_filter_to_list(filters, f"Period= '{period}'")
    if strength != "all str":
        filters = add_filter_to_list(filters, f"Strength= '{strength}'")
    if by_opp != "not op groups":
        query = query + ", Opponent"
        group_bys = group_bys + ", Opponent"
    # adding table to end of query
    query = query + fo_percetnage_query + table
    if len(filters) > 0:
        query = "{0} WHERE {1}".format(query, filters)
    return query + group_bys


ROOT = '/Users/brandonhampstead/Documents/NortheasternHockey'
PATH_TO_DESKTOP= '/Users/brandonhampstead/Desktop/'
DB_TEMP_PATH = f'{ROOT}/faceoff_tracker/src/faceoff_data_model.csv'
FIRST_THIRD_RINK = f'{ROOT}/faceoff_tracker/src/first_and_third_rink.png'
SECOND_RINK = f'{ROOT}/faceoff_tracker/src/second_period_rink.png'

if __name__ == '__main__':

    # creating a dataframe instance
    database_columns_csv = pd.read_csv(
        DB_TEMP_PATH,
        index_col=False)

    # db engine
    engine = sqlalchemy.create_engine('sqlite:///:memory:')

    # storing dataframe in a table
    hockey_faceoff_data_table = database_columns_csv.to_sql('hockey_faceoff_data_table', engine, index=False)

    # variable to save a possible stats dataframe to export to excel
    df_to_export = pd.DataFrame()

    # creating tinker window
    window = tk.Tk()
    window.title("Northeastern Huskies Hockey - Faceoff Tracker")

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

    # packing options widgets
    first_period.grid(row=0, column=1)
    second_period.grid(row=0, column=3)
    third_period.grid(row=0, column=5)
    ot.grid(row=0, column=7)
    even.grid(row=1, column=2)
    pp.grid(row=1, column=4)
    pk.grid(row=1, column=6)

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


    # clear button input frame
    def clear_ents():
        zone.delete(0, END)
        husky.delete(0, END)
        opp.delete(0, END)
        result.delete(0, END)
        zone.focus()


    clear_entries = tk.Button(master=input_frame, text="Clear", command=clear_ents)

    log = tkscrolled.ScrolledText(master=input_frame, width=40, wrap='word')

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
    photo = Image.open(FIRST_THIRD_RINK)
    re_sized_photo = photo.resize((500, 200))
    hockey_rink = ImageTk.PhotoImage(re_sized_photo)
    rink_photo = tk.Label(master=rink_frame, image=hockey_rink)

    sec_photo = Image.open(SECOND_RINK).resize((500, 200))
    second_rink = ImageTk.PhotoImage(sec_photo)

    second_rink_photo = tk.Label(master=rink_frame, image=second_rink)

    # packing rink widgets in rink frame
    rink_photo.pack()
    second_rink_photo.pack()

    # stats frame and widgets
    stats_frame = tk.LabelFrame(text="Display Stats", )
    stats_log = tkscrolled.ScrolledText(master=stats_frame, wrap='word')
    whose_stats = tk.Label(master=stats_frame, text="What Husky's FO stats?")
    what_opp = tk.Label(master=stats_frame, text="Against Who?")
    what_zone = tk.Label(master=stats_frame, text="Zone(1-9)?")
    zone_up = tk.Entry(master=stats_frame, width=2)
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
    give_all_ops = tk.StringVar(value= 'not op groups')
    by_all_ops = tk.Radiobutton(master=stats_frame, text= "By All Ops", value= 'by_all_ops', variable= give_all_ops)
    default_by_ops = tk.Radiobutton(master=stats_frame, text="Normal Ops", value='not op groups', variable=give_all_ops)


    def valid_stats_zone(z):
        if z != "":
            if z not in ZONE_LIST:
                zone_up.delete(0, END)
                zone_up.focus()
            else:
                return ZONE_MAPPING[z]
        else:
            return zone_up.get()


    def display_query():
        per_val = filter_periods.get()
        strength_val = filter_strength.get()
        by_ops_value = give_all_ops.get()
        husky_val = look_up.get()
        opp_val = opp_look_up.get()
        zone_val = valid_stats_zone(zone_up.get())
        # if zone_up.get() != "":
        #     zone_val =ZONE_MAPPING[zone_up.get()]

        # def build_hockey_query(table_name, husky=None,opp=None, period=None, strength=None)
        query = build_hockey_query(table_name='hockey_faceoff_data_table', husky=husky_val,
                                   opp=opp_val, period=per_val, strength=strength_val, zone=zone_val,
                                   by_opp= by_ops_value)
        stats_log.delete("1.0", END)
        display_table = pd.read_sql_query(query, engine)
        stats_log.insert("1.0", display_table.to_markdown(index=False))
        return display_table




    def display_database():
        per_val = filter_periods.get()
        strength_val = filter_strength.get()
        husky_val = look_up.get()
        zone_val = zone_up.get()
        if zone_up.get() != "":
            zone_val = ZONE_MAPPING[zone_up.get()]
        opp_val = opp_look_up.get()
        # def build_hockey_query(table_name, husky=None,opp=None, period=None, strength=None)
        query = build_hockey_query_db(table_name='hockey_faceoff_data_table', husky=husky_val,
                                      opp=opp_val, period=per_val, strength=strength_val, zone=zone_val)
        stats_log.delete("1.0", END)
        display_table = pd.read_sql_query(query, engine)

        stats_log.insert("1.0", display_table.to_markdown(index=False))
        return display_table


    def save_query_to_csv():
        display_query().to_csv(f'{PATH_TO_DESKTOP}query_output.csv',index=False)

    def save_db_log_to_csv():
        display_database().to_csv(f'{PATH_TO_DESKTOP}log_output.csv',index=False)


    run_query = tk.Button(master=stats_frame, text="Run", command=display_query)
    run_db_log = tk.Button(master=stats_frame, text="Run Log", command=display_database)
    save_cur_query = tk.Button(master=stats_frame, text='Save Query', command=save_query_to_csv)
    save_cur_db = tk.Button(master=stats_frame,text= "Save Log", command=save_db_log_to_csv)


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
    default_by_ops.grid(row=3, column=4)
    by_all_ops.grid(row=4, column=4)

    whose_stats.grid(row=4, column=0)
    look_up.grid(row=4, column=1)
    what_opp.grid(row=5, column=0)
    opp_look_up.grid(row=5, column=1)
    what_zone.grid(row=6, column=0)
    zone_up.grid(row=6, column=1)
    run_query.grid(row=7, column=0)
    run_db_log.grid(row=7, column=1)
    stats_log.grid(row=8, columnspan=5)
    save_cur_query.grid(row=7,column=2)
    save_cur_db.grid(row=7, column=3)


    # packing frames
    per_str_frame.pack(side='top', ipady=10)
    rink_frame.pack(side='left', fill='both', expand=True)
    input_frame.pack(side='left', fill='both', expand=True)
    stats_frame.pack(side='left', fill='both', expand=True)

    # focusing on inputs
    zone.focus()


    def valid_zone(e):

        if zone.get() not in ZONE_LIST:
            log.insert("1.0", "Please input a valid zone: 1-9\n")
            zone.delete(0, END)
            zone.focus()
        else:
            husky.focus()


    def valid_husky(e):
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


    def valid_stats_frame_husky(e):
        if not look_up.get().isdigit() and not look_up.get() == "":
            stats_log.insert("1.0", "Please input a valid husky jersey\n")
            look_up.delete(0, END)
            look_up.focus()
        else:
            opp_look_up.focus()


    def valid_stats_frame_opp(e):
        if not opp_look_up.get().isdigit() and not opp_look_up.get() == "":
            stats_log.insert("1.0", "Please input a valid opponent jersey number\n")
            opp_look_up.delete(0, END)
            opp_look_up.focus()
        else:
            zone_up.focus()


    def add_FO(e):
        # use csv as rdb to add this faceoff as a single entry with
        # period, player, opp, str, zone(mapped), result

        # if opp is "" / none then go for all opps
        if result.get().upper() not in ['W', 'L']:
            log.insert("1.0", "Please input a valid result: W , L \n")
            result.delete(0, END)
            result.focus()
        else:
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
                                 formatted_zone, result.get().upper())])
            # print(pd.read_sql_query(f'SELECT * FROM hockey_faceoff_data_table', engine))
            # query = 'SELECT  player, count(result) AS "wins", zone FROM hockey_faceoff_data_table
            # WHERE result="w"  GROUP BY Player, Zone '
            # print(pd.read_sql_query(query, engine))

            log.insert("1.0",
                       f"{formatted_period}: {husky.get()} vs {opp.get()} in zone {formatted_zone}: "
                       f"{result.get().upper()}\n")

            clear_ents()


    # binding input frame entry boxes
    zone.bind("<Return>", valid_zone)
    husky.bind("<Return>", valid_husky)
    opp.bind("<Return>", valid_opp)
    result.bind("<Return>", add_FO)

    # binding stats entry boxes
    look_up.bind("<Return>", valid_stats_frame_husky)
    opp_look_up.bind("<Return>", valid_stats_frame_opp)

    window.mainloop()
