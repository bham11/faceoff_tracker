import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.scrolledtext as tkscrolled
from hockey_db import HockeyDatabase


class GameViewerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Northeastern Huskies Hockey - View Game")
        self.load_frame = LoadFrame(self)
        

        self._pack_frames()
        
    
    def _pack_frames(self):
        self.geometry("1050x500")
        self.load_frame.grid(column=0, row=0, ipadx=10, sticky=NW)
        

class LoadFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "Load Game Log")
        self.scrollbar = Scrollbar(master=self, orient=HORIZONTAL)
        self.display_file_name = tk.Entry(master=self, xscrollcommand=self.scrollbar.set)
        self.insert_filename = tk.Entry(master=self)
        self.game_file_name = tk.Button(master=self, text="Select Game", command=self.get_filename)
        self.send_button = tk.Button(master=self, text="Load Data", command=self.load_game_data)
        self.stats_log = tkscrolled.ScrolledText(master=self, wrap='word')
        
        self._pack_widgets()
        
    def _pack_widgets(self):
        self.game_file_name.grid(row=1,column=1)
        self.display_file_name.grid(row=2,column=1)
        self.scrollbar.config(command=self.display_file_name.xview)
        self.send_button.grid(row=3,column=1)
        self.stats_log.tag_configure("center", justify='center')
        self.stats_log.grid(row=4,column=1)
        
    
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
    
    def load_game_data(self):
        table = HockeyDatabase(self.insert_filename.get())

        query = table.build_hockey_query('hockey_faceoff_data_table', "", "", "all per", "all str", "", "not op groups")
        # query = "SELECT * from hockey_faceoff_data_table"
        self.stats_log.delete("1.0", END)
        display_table = table.return_query_df(query)
        self.stats_log.insert("1.0", display_table.to_markdown(index=False))
        self.stats_log.tag_add("center", "1.0", "end")
        return table.return_query_df(query)
   
 
if __name__ == '__main__':
    window = GameViewerWindow()
    window.mainloop()