# Northeastern University Men's Hockey Face Off Tracker
By: Brandon Hampstead

## <ins> Purpose <ins>
- This program allows for the collection of detailed face-off statistics with the ability to display stats based of opponent, zone, period, and strength.

## <ins> Initial Setup <ins>
1. Upon downloading this project folder, via .zip or Github, you will need to have python 3.10 as a start.
2. Go into the terminal, navigate (using "cd") to where you placed the "faceoff_tracker" folder on your computer
3. Once in the faceoff_tracker" folder, type <code> open src/database_gui_main.py</code> and the file will open.
   - At this point find line 81 and change the <code> ROOT</code> variable to the local path to that folder on your computer, make sure to save this 
## <ins> Average Startup <ins>
1. This program comes equipped with a <code>makefile</code> to setup the venv and run the program from the command line
2. First run <code>make venv</code> to create the virutal enviroment
3. Then run <code>make install</code> to install the required packages found in <code>requirements.txt</code>
4. Finally, run <code> make run</code> to start the GUI and statistics capturing

## <ins> Capturing Face Off data <ins>
- This program is broken into mainly two parts, or windows:
  - The Inputs frame and options frame: this is where you input faceoff data. Make sure the period and ice strength around updated by clicking the radio buttons accordingly

