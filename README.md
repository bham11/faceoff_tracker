# Northeastern University Men's Hockey Face Off Tracker
By: Brandon Hampstead

## <ins> Purpose <ins>
- This program allows for the collection of detailed face-off statistics with the ability to display stats based of opponent, zone, period, and strength.

## <ins> Initial Setup <ins>
1. Upon downloading this project folder, via .zip or Github, you will need to have python 3.10 as a start.
2. Go into the terminal, navigate (using "cd") to where you placed the "faceoff_tracker" folder on your computer
3. Once in the faceoff_tracker" folder, type <code> open src/database_gui_main.py</code> and the file will open.
   - At this point find line 81 and change the <code> ROOT</code> variable to the local path to that folder on your computer, make sure to save this 
   - Make sure to change <code> PATH_TO_DESKTOP </code> variable to your desktop as well, since this is where the output files will be saved
## <ins> Average Startup <ins>
1. This program comes equipped with a <code>makefile</code> to setup the venv and run the program from the command line
2. First run <code>make venv</code> to create the virutal enviroment
3. Then run <code>make install</code> to install the required packages found in <code>requirements.txt</code>
4. Finally, run <code> make run</code> to start the GUI and statistics capturing

## <ins> Capturing Face Off data <ins>
- This program is broken into mainly two parts, or windows:
  - The Inputs frame and options frame: this is where you input faceoff data. Make sure the period and ice strength around updated by clicking the radio buttons accordingly. 
    - Input the zone (1-9 mapped from the pictures to the left of the Inputs Frame) and hit enter. 
    - Then input the jersey number of the Husky that is taking the faceoff and hit enter. 
    - Then input the jersey number of the Opponent that took the faceoff and hit enter. 
    - Finally, input W or L depending if our guy won the draw.
  - The Stats frame has period and strength options to specify what type of face offs you want to select from.
    - If you want to select from all face off data, leave the "All Periods" and "All Strengths" radio buttons selected.
    - There are text boxes to specify which Husky, which zone, and which Opponent to "filter on"
    - Hit the <code> Run</code> button to see the Wins/Totals for the based of the selected parameters. 
    - Hit the <code> Run Log</code> button to see the Logsfor the based of the selected parameters.
  - You can save both the log and the current query to your desktop with the Save buttons on the pane.

