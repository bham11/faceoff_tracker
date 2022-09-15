


all: install run


install: venv
	: # Activate venv and install smthing inside
	 source venv/bin/activate && pip3 install -r requirements.txt


run:
	. venv/bin/activate && pip3 -V && python3 src/database_gui_main.py

venv:
	: # Create venv if it doesn't exist
	test -d venv || python3 -m venv venv

clean:
	rm -rf venv
	find . -iname "*.pyc" -delete