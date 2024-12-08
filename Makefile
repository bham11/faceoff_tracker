


# all: install run


# install: venv
# 	: # Activate venv and install smthing inside
# 	 source venv/bin/activate && pip3 install -r requirements.txt


# run:
# 	. venv/bin/activate && pip3 -V && python3 src/v1/database_gui_main.py

# run-v2:
# 	. venv/bin/activate && cd src/v2 pip3 -V && python3 main.py

# run-db:
# 	. venv/bin/activate && cd src/v2 pip3 -V && python3 insert_gui.py

# run-single:
# 	. venv/bin/activate && cd src/v2 pip3 -V && python3 single_game_gui.py

# venv:
# 	: # Create venv if it doesn't exist
# 	test -d venv || python3 -m venv venv

clean-old:
	rm -rf venv
	find . -iname "*.pyc" -delete


# Define the name of the virtual environment directory
VENV_DIR = .venv

# Define the Python version (for making sure the virtual environment uses Python 3.10)
PYTHON_VERSION = python3.10

# Define the command to create the virtual environment
VENV_CMD = $(PYTHON_VERSION) -m venv $(VENV_DIR)

# Define the command to activate the virtual environment
ACTIVATE_VENV = source $(VENV_DIR)/bin/activate

# Define the command to install dependencies using Poetry
INSTALL_CMD = poetry install

# Create the virtual environment and install dependencies
setup: $(VENV_DIR)/bin/activate
	$(ACTIVATE_VENV) && $(INSTALL_CMD)

# Create the virtual environment
$(VENV_DIR)/bin/activate: 
	$(VENV_CMD)
	touch $(VENV_DIR)/bin/activate


.PHONY: install
install:
	poetry install

.PHONY: build
build:
	poetry build

.PHONY: clean
clean:
	rm -rf dist

.PHONY: lint
lint:
	poetry run flake8

.PHONY: format
format:
	poetry run black .

.PHONY: activate-venv
activate-venv:
	source .venv/bin/activate

run-v2:
	cd src/v2 && poetry run python3 main.py

run-db:
	cd src/v2 && poetry run python3 insert_gui.py

run-single:
	cd src/v2 && poetry run python3 single_game_gui.py


