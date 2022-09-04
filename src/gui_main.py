import tkinter as tk
from tkinter import END

from src.faceoff_data import HUSKIES, ZONE_MAPPING
from PIL import ImageTk, Image

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Northeastern Huskies Hockey - Faceoff Tracker")

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


    clear_entries = tk.Button(master=input_frame, text="Clear", command=clear_ents)

    log = tk.Text(master=input_frame)

    photo = Image.open("hockey_rink.png")
    # TODO: do this in the photo
    # re_sized_photo = photo.resize((500, 500))
    # rotated = re_sized_photo.rotate(90)
    hockey_rink = ImageTk.PhotoImage(photo)
    rink_photo = tk.Label(master=input_frame, image=hockey_rink)

    rink_photo.pack()
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

    input_frame.pack()

    zone.focus()
    zone.bind("<Return>", lambda funct1: husky.focus())
    husky.bind("<Return>", lambda funct1: opp.focus())
    opp.bind("<Return>", lambda funct1: result.focus())


    def add_FO(e):
        if HUSKIES[husky.get()]["vs"].get(opp.get(), None) is None:
            HUSKIES[husky.get()]["vs"][opp.get()] = {"w": 0, "l": 0}
        HUSKIES[husky.get()]["vs"][opp.get()][result.get().lower()] += 1
        log.insert("1.0", f"{husky.get()} vs {opp.get()} in zone: {ZONE_MAPPING[zone.get()]}: {result.get()}\n")


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
