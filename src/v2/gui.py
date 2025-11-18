import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tkscrolled
from PIL import ImageTk, Image
from datetime import date

from constants import ROOT

ZONE_MAPPING = {
    "1": "RO",
    "2": "LO",
    "3": "RONZ",
    "4": "LONZ",
    "5": "C",
    "6": "LDNZ",
    "7": "RDNZ",
    "8": "LD",
    "9": "RD",
}

ZONE_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


class HockeyWindow(tk.Tk):

    def __init__(self, database):
        super().__init__()
        self.title("Northeastern Huskies Hockey - Faceoff Tracker")
        self.game_info_frame = GameInfoFrame(self)
        self.faceoff_input_frame = FaceoffInputFrame(
            self, database, self.game_info_frame
        )
        self.rink_frame = RinkFrame(self)
        self.stats_frame = StatsFrame(self, database)

        self.database = database

        self._pack_frames()

    def _pack_frames(self):
        self.game_info_frame.pack(side="top", ipady=10)
        self.rink_frame.pack(side="left", fill="both", expand=True)
        self.faceoff_input_frame.pack(side="left", fill="both", expand=True)
        self.stats_frame.pack(side="left", fill="both", expand=True)


class GameInfoFrame(tk.LabelFrame):

    def __init__(self, container):
        super().__init__(container, text="Options")

        self.what_period = tk.StringVar(value="1rst")
        self.first_period = tk.Radiobutton(
            master=self, text="1rst", value="1rst", variable=self.what_period
        )
        self.second_period = tk.Radiobutton(
            master=self, text="2nd", value="2nd", variable=self.what_period
        )
        self.third_period = tk.Radiobutton(
            master=self, text="3rd", value="3rd", variable=self.what_period
        )
        self.ot = tk.Radiobutton(
            master=self, text="OT", value="OT", variable=self.what_period
        )
        self.strength = tk.StringVar(value="even")
        self.even = tk.Radiobutton(
            master=self, text="Even", value="even", variable=self.strength
        )
        self.pk = tk.Radiobutton(
            master=self, text="PK", value="pk", variable=self.strength
        )
        self.pp = tk.Radiobutton(
            master=self, text="PP", value="pp", variable=self.strength
        )

        self._pack_widgets()

    def _pack_widgets(self):
        self.first_period.grid(row=0, column=1)
        self.second_period.grid(row=0, column=3)
        self.third_period.grid(row=0, column=5)
        self.ot.grid(row=0, column=7)
        self.even.grid(row=1, column=2)
        self.pp.grid(row=1, column=4)
        self.pk.grid(row=1, column=6)


class FaceoffInputFrame(tk.LabelFrame):
    def __init__(self, container, database, options_frame):
        super().__init__(container, text="Inputs:")

        self.database = database
        self.options = options_frame

        self.config(width=200)
        self.what_zone = tk.Label(master=self, text="What Zone (1-9)?")
        self.zone = tk.Entry(master=self, width=2)
        self.what_husky = tk.Label(master=self, text="What Husky?")
        self.husky = tk.Entry(master=self, width=2)
        self.what_opp = tk.Label(master=self, text="What Opp?")
        self.opp = tk.Entry(master=self, width=2)
        self.ask_result = tk.Label(master=self, text="Result (W/L)?")
        self.result = tk.Entry(master=self, width=2)

        self.clear_entries = tk.Button(
            master=self, text="Clear", command=self.clear_ents
        )

        self.log = tkscrolled.ScrolledText(master=self, width=40, wrap="word")

        self._pack_widgets()

        self._bind_inputs()

        self.zone.focus()

    def clear_ents(self):
        self.zone.delete(0, END)
        self.husky.delete(0, END)
        self.opp.delete(0, END)
        self.result.delete(0, END)
        self.zone.focus()

    def _pack_widgets(self):
        self.what_zone.grid(row=1, column=1)
        self.zone.grid(row=1, column=2)
        self.what_husky.grid(row=2, column=1)
        self.husky.grid(row=2, column=2)
        self.what_opp.grid(row=3, column=1)
        self.opp.grid(row=3, column=2)
        self.ask_result.grid(row=4, column=1)
        self.result.grid(row=4, column=2)
        self.clear_entries.grid(row=5, column=2)
        self.log.grid(row=6, columnspan=5)

    def valid_zone(self, e):

        if self.zone.get() not in ZONE_LIST:
            self.log.insert("1.0", "Please input a valid zone: 1-9\n")
            self.zone.delete(0, END)
            self.zone.focus()
        else:
            self.husky.focus()

    def valid_husky(self, e):
        if not self.husky.get().isdigit():
            self.log.insert("1.0", "Please input a valid husky jersey\n")
            self.husky.delete(0, END)
            self.husky.focus()
        else:
            self.opp.focus()

    def valid_opp(self, e):
        if not self.opp.get().isdigit():
            self.log.insert("1.0", "Please input a valid opponent jersey number\n")
            self.opp.delete(0, END)
            self.opp.focus()
        else:
            self.result.focus()

    def add_FO(self, e):
        # use csv as rdb to add this faceoff as a single entry with
        # period, player, opp, str, zone(mapped), result

        # if opp is "" / none then go for all opps
        if self.result.get().upper() not in ["W", "L"]:
            self.log.insert("1.0", "Please input a valid result: W , L \n")
            self.result.delete(0, END)
            self.result.focus()
        else:
            period_map = {"1rst": "P1", "2nd": "P2", "3rd": "P3", "OT": "OT"}
            formatted_period = period_map[self.options.what_period.get()]
            formatted_zone = ZONE_MAPPING[self.zone.get()]
            self.database.insert_faceoff(
                self.options.what_period.get(),
                self.husky.get(),
                self.opp.get(),
                self.options.strength.get(),
                formatted_zone,
                self.result.get().upper(),
            )

            self.log.insert(
                "1.0",
                f"{formatted_period}: {self.husky.get()} vs {self.opp.get()} in zone {formatted_zone}: "
                f"{self.result.get().upper()}\n",
            )

            self.clear_ents()

    def _bind_inputs(self):
        self.zone.bind("<Return>", self.valid_zone)
        self.husky.bind("<Return>", self.valid_husky)
        self.opp.bind("<Return>", self.valid_opp)
        self.result.bind("<Return>", self.add_FO)


class RinkFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text="Rink Mappings")

        first_third = f"{ROOT}/utils/first_and_third_rink.png"
        second = f"{ROOT}/utils/second_period_rink.png"
        photo = Image.open(first_third)
        re_sized_photo = photo.resize((500, 200))
        sec_photo = Image.open(second).resize((500, 200))
        self.hockey_rink = ImageTk.PhotoImage(re_sized_photo)
        self.second_rink = ImageTk.PhotoImage(sec_photo)

        self.rink_photo = tk.Label(self, image=self.hockey_rink)
        self.second_rink_photo = tk.Label(self, image=self.second_rink)

        self._pack_widgets()

    def _pack_widgets(self):
        self.rink_photo.pack()
        self.second_rink_photo.pack()


class StatsFrame(tk.LabelFrame):
    def __init__(self, container, database):
        super().__init__(container, text="Display Stats")

        self.database = database

        self.stats_log = tkscrolled.ScrolledText(master=self, wrap="word")
        self.whose_stats = tk.Label(master=self, text="What Husky's FO stats?")
        self.what_opp = tk.Label(master=self, text="Against Who?")
        self.what_zone = tk.Label(master=self, text="Zone(1-9)?")
        self.zone_up = tk.Entry(master=self, width=2)
        self.look_up = tk.Entry(master=self, width=2)
        self.opp_look_up = tk.Entry(master=self, width=2)

        self.filter_periods = tk.StringVar(value="all per")
        self.filter_first_period = tk.Radiobutton(
            master=self, text="1rst", value="1rst", variable=self.filter_periods
        )
        self.filter_second_period = tk.Radiobutton(
            master=self, text="2nd", value="2nd", variable=self.filter_periods
        )
        self.filter_third_period = tk.Radiobutton(
            master=self, text="3rd", value="3rd", variable=self.filter_periods
        )
        self.filter_ot = tk.Radiobutton(
            master=self, text="OT", value="OT", variable=self.filter_periods
        )
        self.filter_all_periods = tk.Radiobutton(
            master=self, text="All Per", value="all per", variable=self.filter_periods
        )
        self.filter_strength = tk.StringVar(value="all str")
        self.filter_even = tk.Radiobutton(
            master=self, text="Even", value="even", variable=self.filter_strength
        )
        self.filter_pk = tk.Radiobutton(
            master=self, text="PK", value="pk", variable=self.filter_strength
        )
        self.filter_pp = tk.Radiobutton(
            master=self, text="PP", value="pp", variable=self.filter_strength
        )
        self.filter_all_strengths = tk.Radiobutton(
            master=self, text="All Strs", value="all str", variable=self.filter_strength
        )
        self.give_all_ops = tk.StringVar(value="not op groups")
        self.by_all_ops = tk.Radiobutton(
            master=self,
            text="By All Ops",
            value="by_all_ops",
            variable=self.give_all_ops,
        )
        self.default_by_ops = tk.Radiobutton(
            master=self,
            text="Normal Ops",
            value="not op groups",
            variable=self.give_all_ops,
        )

        self.run_query = tk.Button(master=self, text="Run", command=self.display_query)
        self.run_db_log = tk.Button(
            master=self, text="Run Log", command=self.display_database
        )
        self.save_cur_query = tk.Button(
            master=self, text="Save Query", command=self.save_query_to_csv
        )
        self.save_cur_db = tk.Button(
            master=self, text="Save Log", command=self.save_db_log_to_csv
        )

        self._pack_widgets()

    def _pack_widgets(self):
        self.filter_all_periods.grid(row=0, column=0)
        self.filter_first_period.grid(row=0, column=1)
        self.filter_second_period.grid(row=0, column=2)
        self.filter_third_period.grid(row=0, column=3)
        self.filter_ot.grid(row=0, column=4)
        self.filter_all_strengths.grid(row=3, column=0)
        self.filter_even.grid(row=3, column=1)
        self.filter_pp.grid(row=3, column=2)
        self.filter_pk.grid(row=3, column=3)
        self.default_by_ops.grid(row=3, column=4)
        self.by_all_ops.grid(row=4, column=4)
        self.whose_stats.grid(row=4, column=0)
        self.look_up.grid(row=4, column=1)
        self.what_opp.grid(row=5, column=0)
        self.opp_look_up.grid(row=5, column=1)
        self.what_zone.grid(row=6, column=0)
        self.zone_up.grid(row=6, column=1)
        self.run_query.grid(row=7, column=0)
        self.run_db_log.grid(row=7, column=1)
        self.save_cur_query.grid(row=7, column=2)
        self.save_cur_db.grid(row=7, column=3)
        self.stats_log.grid(row=8, columnspan=5)

    def _bind_inputs(self):
        self.look_up.bind("<Return>", self.valid_stats_frame_husky)
        self.opp_look_up.bind("<Return>", self.valid_stats_frame_opp)

    def valid_stats_zone(self, z):
        if z != "":
            if z not in ZONE_LIST:
                self.zone_up.delete(0, END)
                self.zone_up.focus()
            else:
                return ZONE_MAPPING[z]
        else:
            return self.zone_up.get()

    def valid_stats_frame_husky(self, e):
        if not self.look_up.get().isdigit() and not self.look_up.get() == "":
            self.stats_log.insert("1.0", "Please input a valid husky jersey\n")
            self.look_up.delete(0, END)
            self.look_up.focus()
        else:
            self.opp_look_up.focus()

    def valid_stats_frame_opp(self, e):
        if not self.opp_look_up.get().isdigit() and not self.opp_look_up.get() == "":
            self.stats_log.insert(
                "1.0", "Please input a valid opponent jersey number\n"
            )
            self.opp_look_up.delete(0, END)
            self.opp_look_up.focus()
        else:
            self.zone_up.focus()

    def display_query(self):
        per_val = self.filter_periods.get()
        strength_val = self.filter_strength.get()
        by_ops_value = self.give_all_ops.get()
        husky_val = self.look_up.get()
        opp_val = self.opp_look_up.get()
        zone_val = self.valid_stats_zone(self.zone_up.get())
        # if zone_up.get() != "":
        #     zone_val =ZONE_MAPPING[zone_up.get()]

        # def build_hockey_query(table_name, husky=None,opp=None, period=None, strength=None)
        query = self.database.build_hockey_query(
            table_name="hockey_faceoff_data_table",
            husky=husky_val,
            opp=opp_val,
            period=per_val,
            strength=strength_val,
            zone=zone_val,
            by_opp=by_ops_value,
        )
        self.stats_log.delete("1.0", END)
        display_table = self.database.return_query_df(query)
        self.stats_log.insert("1.0", display_table.to_markdown(index=False))
        return display_table

    def display_database(self):
        per_val = self.filter_periods.get()
        strength_val = self.filter_strength.get()
        husky_val = self.look_up.get()
        zone_val = self.zone_up.get()
        if self.zone_up.get() != "":
            zone_val = ZONE_MAPPING[self.zone_up.get()]
        opp_val = self.opp_look_up.get()
        # def build_hockey_query(table_name, husky=None,opp=None, period=None, strength=None)
        query = self.database.build_hockey_query_db(
            table_name="hockey_faceoff_data_table",
            husky=husky_val,
            opp=opp_val,
            period=per_val,
            strength=strength_val,
            zone=zone_val,
        )
        self.stats_log.delete("1.0", END)
        display_table = self.database.return_query_df(query)

        self.stats_log.insert("1.0", display_table.to_markdown(index=False))
        return display_table

    def save_query_to_csv(self):
        self.database.save_df_to_csv(self.display_query(), "query_output")

    def save_db_log_to_csv(self):
        today = date.today().strftime("%m_%d_%Y")
        self.database.save_df_to_csv(self.display_database(), f"{today}_log_output")
