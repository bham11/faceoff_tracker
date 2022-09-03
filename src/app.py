import tkinter as tk

from src.faceoff_data import HUSKIES, ZONE_MAPPING


class app(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Northeastern Huskies Hockey - Faceoff Tracker")
        app.make_stats_widgets(self)
        app.bind_stats_buttons_to_enter(self)
        self.root.mainloop()

    def _add_FO(self, e):
        HUSKIES[self.husky.get()]["vs"][self.opp.get()][self.result.get()] += 1

    def make_stats_widgets(self):
        self.what_zone = tk.Label(text="What Zone (1-9)?")
        self.zone = tk.Entry()

        self.what_husky = tk.Label(text="What Husky?")
        self.husky = tk.Entry()

        self.what_opp = tk.Label(text="What Opp?")
        self.opp = tk.Entry()

        self.ask_result = tk.Label(text="Result (W/L)?")
        self.result = tk.Entry()

        self.what_zone.pack()
        self.zone.pack()
        self.what_husky.pack()
        self.husky.pack()
        self.what_opp.pack()
        self.opp.pack()
        self.ask_result.pack()
        self.result.pack()

    def bind_stats_buttons_to_enter(self):
        self.zone.focus()
        self.zone.bind("<Return>", lambda funct1: self.husky.focus())
        self.husky.bind("<Return>", lambda funct1: self.opp.focus())
        self.opp.bind("<Return>", lambda funct1: self.result.focus())
        self.result.bind("<Return>", app._add_FO(self))


app()
