import tkinter as tk
from tkinter import END, BOTTOM, NONE

import pandas as pd

from src.faceoff_data import ZONE_MAPPING, HUSKIES
from PIL import ImageTk, Image

if __name__ == '__main__':

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

    rink_photo.pack()
    rink_frame.pack(side="top")

    # stats frame and widgets
    stats_frame = tk.Frame()
    slog_scrollbar = tk.Scrollbar(stats_frame, orient="horizontal")
    stats_log = tk.Text(master=stats_frame, wrap=NONE, xscrollcommand=slog_scrollbar.set)
    whose_stats = tk.Label(master=stats_frame, text="What Husky's FO stats?")
    look_up = tk.Entry(master=stats_frame)


    def display_stats():
        center_list = ['10', '27', '29', '7', '15']
        if not look_up.get() in HUSKIES.keys():
            stats_log.insert("1.0", "Please input a valid husky\n")
            look_up.delete(0, END)
            stats_log.delete("2.0", END)
            look_up.focus()
        else:
            data = pd.DataFrame.from_dict(data=HUSKIES[look_up.get()]["vs"])
            stats_log.delete("1.0", END)
            stats_log.insert("1.0", f"{data.to_markdown()}\n")


    def display_percentage():
        center_list = ['10', '27', '29', '7', '15']
        if not str(look_up.get()) in HUSKIES.keys():
            stats_log.insert("1.0", "Please input a valid husky\n")
            look_up.delete(0, END)
            stats_log.delete("2.0", END)
            look_up.focus()

        else:
            # each guys zone percentage on the same table. specific columns and rows
            data = pd.DataFrame(data=HUSKIES[look_up.get()])
            for key in HUSKIES[look_up.get()]["vs"]:
                data = data.drop(key, axis=0)
            data = data.drop('vs', axis=1)
            data = data.applymap(lambda perc: str(perc * 100) + '%')
            stats_log.delete("1.0", END)
            stats_log.insert("1.0", f"{data.to_markdown()}\n")


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
        if result.get().lower() not in ['w', 'l']:
            log.insert("1.0", "Please input a valid result (W or L)\n")
            result.delete(0, END)
            result.focus()
        else:
            if HUSKIES.get(husky.get(), None) is None:
                HUSKIES[husky.get()] = {
                    "vs": {

                    },
                    "zone%": {
                        "LD": 0,
                        "RD": 0,
                        "RO": 0,
                        "LO": 0,
                        "C": 0,
                        "LDNZ": 0,
                        "RDNZ": 0,
                        "LONZ": 0,
                        "RONZ": 0,
                    }
                }
            if HUSKIES[husky.get()]["vs"].get(opp.get(), None) is None:
                HUSKIES[husky.get()]["vs"][opp.get()] = {
                    "LD": {"w": 0, "l": 0},
                    "RD": {"w": 0, "l": 0},
                    "RO": {"w": 0, "l": 0},
                    "LO": {"w": 0, "l": 0},
                    "C": {"w": 0, "l": 0},
                    "LDNZ": {"w": 0, "l": 0},
                    "RDNZ": {"w": 0, "l": 0},
                    "LONZ": {"w": 0, "l": 0},
                    "RONZ": {"w": 0, "l": 0},
                    "TOTAL": {"w": 0, "l": 0},
                }

            # adding FO to 'vs' dict
            formatted_zone = ZONE_MAPPING[zone.get()]
            prefix_zone = HUSKIES[husky.get()]["vs"][opp.get()][formatted_zone]
            prefix_total = HUSKIES[husky.get()]["vs"][opp.get()]["TOTAL"]
            prefix_zone[result.get().lower()] += 1
            prefix_total[result.get().lower()] += 1

            # adding FO to 'zone%' dict
            decimal = prefix_zone['w'] / (prefix_zone['w'] + prefix_zone['l'])
            HUSKIES[husky.get()]['zone%'][formatted_zone] = decimal

            log.insert("1.0", f"{husky.get()} vs {opp.get()} in zone {formatted_zone}: {result.get()}\n")

            clear_ents()


    zone.bind("<Return>", valid_zone)
    husky.bind("<Return>", valid_husky)
    opp.bind("<Return>", valid_opp)
    result.bind("<Return>", add_FO)

    window.mainloop()
