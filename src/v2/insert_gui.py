import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.scrolledtext as tkscrolled
from insert_db import insert_game, OPPONENTS, select_opponent_data



class InsertDataWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Northeastern Huskies Hockey - Insert Game into Database 2023-2024")
        self.file_frame = FileFrame(self)
        self.query_frame = QueryFrame(self)
        
        

        self._pack_frames()
        
    
    def _pack_frames(self):
        self.geometry("1050x500")
        self.file_frame.grid(column=0, row=0, ipadx=10, sticky=NW)
        self.query_frame.grid(column=15, row=0)
        
        

class FileFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "Insert Game File")
        self.opponent_box = ttk.Combobox(master=self,state="readonly", values = OPPONENTS, height=5)
        self.select_opponent = tk.Label(master=self, text="Select Opponent:")
        self.scrollbar = Scrollbar(master=self, orient=HORIZONTAL)
        self.display_file_name = tk.Entry(master=self, xscrollcommand=self.scrollbar.set)
        self.insert_filename = tk.Entry(master=self)
        self.game_file_name = tk.Button(master=self, text="Select Game", command=self.get_filename)
        self.send_button = tk.Button(master=self, text="Insert Data", command=self.send_game_data)
        
        
        
        
        
        self._pack_widgets()
        
    def get_filename(self):
        value = filedialog.askopenfilename()
        if value:
            show_value = value.rsplit("/", 1)[1]
            self.insert_filename.delete(0,END)
            self.insert_filename.insert(0, value)
            self.display_file_name.config(foreground="black")
            self.display_file_name.delete(0, END)
            self.display_file_name.insert(0, show_value)
        return value
        
        
    def send_game_data(self):
        # this needs to be full file name but i just want to show trucated value
        game_log = self.insert_filename.get()
        if game_log.endswith(".csv"):
            insert_game("2023-2024/production.db", self.opponent_box.get(), game_log)
            self.display_file_name.config(foreground="green")
        else:
            self.display_file_name.config(fg="red")
        
    def _pack_widgets(self):
        self.select_opponent.grid(row=1,column=0)
        self.opponent_box.grid(row=11, column=0)
        self.display_file_name.grid(row=30, column=0,)
        self.scrollbar.grid(row=32, column=0)
        self.scrollbar.config(command=self.display_file_name.xview)
        self.game_file_name.grid(row=34, column=0)
        self.send_button.grid(row=36, column=0)
    
class QueryFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "View Opponent:")
        self.select_opponent = tk.Label(master=self, text="Select Team:")
        self.opponent_box = ttk.Combobox(master=self,state="readonly", values = OPPONENTS, height=5)
        self.log_display = tkscrolled.ScrolledText(master=self, wrap='word', )
        self.view_button = tk.Button(master=self, text="View Data", command=self.get_game_data)
        self.group_by_opp = tk.BooleanVar(value=False)
        self.group_by_opp_radio = tk.Radiobutton(master=self, text= "by opp", value=True, variable=self.group_by_opp)
        self.group_by_strength = tk.BooleanVar(value=False)
        self.group_by_strength_radio = tk.Radiobutton(master=self, text= "by strength", value=True, variable=self.group_by_strength)
        self.group_by_period = tk.BooleanVar(value=False)
        self.group_by_period_radio = tk.Radiobutton(master=self, text= "by period", value=True, variable=self.group_by_period)
        self.group_by_zone = tk.BooleanVar(value=False)
        self.group_by_zone_radio = tk.Radiobutton(master=self, text= "by zone", value=True, variable=self.group_by_zone)
        self.opp_where = tk.Label(master=self, text="Select Opponent:")
        self.opponent_input = tk.Entry(master=self, width=2)
        
        self._pack_widgets()
        
    def _pack_widgets(self):
        self.select_opponent.grid(row=0,column=2)
        self.group_by_opp_radio.grid(row=1, column=0, ipadx=18)
        self.group_by_strength_radio.grid(row=2, column=0, ipadx=5)
        self.group_by_period_radio.grid(row=3, column=0, ipadx=11)
        self.group_by_zone_radio.grid(row=4, column=0, ipadx=16)
        self.opp_where.grid(row=3, column=3)
        self.opponent_input.grid(row=4, column=3)
        self.opponent_box.grid(row=2,column=2)
        self.view_button.grid(row=3,column=2)
        self.log_display.grid(row=7, column=2)
        
    def get_add_fields(self):
        return []  
    
    def get_query_params(self):
        group_list = []
        add_fields_list = []
        where_filters =[]
        if self.group_by_opp.get():
            group_list.append("opponent")
            add_fields_list.append("opponent")
            self.group_by_opp.set(False)
        if self.group_by_strength.get():
            group_list.append("strength")
            add_fields_list.append("strength")
            self.group_by_strength.set(False)
        if self.group_by_period.get():
            group_list.append("period")
            add_fields_list.append("period")
            self.group_by_period.set(False)
        if self.group_by_zone.get():
            group_list.append("zone")
            add_fields_list.append("zone")
            self.group_by_zone.set(False)
        if self.opponent_input.get().isdigit():
            jersey = self.opponent_input.get()
            add_fields_list.append("opponent")
            where_filters.append(f"Opponent = {jersey}")
            self.opponent_input.delete(0,END)
            
            
            
        return add_fields_list , group_list, where_filters 
        
    def get_game_data(self):
        opponent = self.opponent_box.get()
        add_fields, groups, filters = self.get_query_params()
        display_table = select_opponent_data("2023-2024/production.db", opponent, add_fields, groups, filters)
        self.log_display.delete("1.0", END)
        self.log_display.insert("1.0", display_table.to_markdown(index=False))
        
        
        return display_table
        
        
        
        
if __name__ == '__main__':
    window = InsertDataWindow()
    
    window.mainloop()
    
    