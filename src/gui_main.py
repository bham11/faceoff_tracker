import tkinter as tk
from tkinter import END

from src.faceoff_data import HUSKIES, ZONE_MAPPING
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

    log = tk.Text(master=input_frame, height= 50, width= 50)

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
    photo = Image.open("vert-hockey-rink.png")
    re_sized_photo = photo.resize((200,500))
    hockey_rink = ImageTk.PhotoImage(re_sized_photo)
    rink_photo = tk.Label(master=rink_frame, image=hockey_rink)

    rink_photo.pack()
    rink_frame.pack(side="top")

    # stats frame and widgets
    stats_frame = tk.Frame()
    stats_log = tk.Text(master=stats_frame)
    whose_stats = tk.Label(master=stats_frame, text="What Husky's FO stats?")
    look_up = tk.Entry(master=stats_frame)

    whose_stats.pack()
    look_up.pack()
    stats_log.pack()
    stats_frame.pack(side="left")

    def display_stats(e):
        pass

    look_up.bind("<Enter>", display_stats)




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
        if husky.get() not in center_list:
            log.insert("1.0", "Please input a valid husky: 10, 27, 29, 7, 15\n")
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
                }
            formatted_zone = ZONE_MAPPING[zone.get()]
            HUSKIES[husky.get()]["vs"][opp.get()][formatted_zone][result.get().lower()] += 1
            log.insert("1.0", f"{husky.get()} vs {opp.get()} in zone {formatted_zone}: {result.get()}\n")

            # adding stats to pandas dataframe


            clear_ents()


    zone.bind("<Return>", valid_zone)
    husky.bind("<Return>", valid_husky)
    opp.bind("<Return>", valid_opp)
    result.bind("<Return>", add_FO)

    window.mainloop()

    # zone_var = ZONE_MAPPING[zone.get()]
    # # ask for opponents centers
    # ops = input("Add opponents centers #'s followed by a space:\n")
    # ops_nums = ops.split(" ")
    #
    # # add opps centers #s into our vs for each of our guys
    # for key in HUSKIES:
    #     for num in ops_nums:
    #         HUSKIES[key]["vs"][num] = {"w": 0, "l": 0}

    # # faceoff time
    # zone = input("What zone (1-9)?\n")
    # husky = input("What Husky?\n")
    # other_guy = input("What opp center?\n")
    # result = input("Result (W/L)?\n")

    # # adding stats
    # # TODO: Add try block
    # HUSKIES[husky]["vs"][other_guy][result] += 1
    # mapped_zone = ZONE_MAPPING[zone]
    # HUSKIES[husky]["zone"][mapped_zone][result] += 1
