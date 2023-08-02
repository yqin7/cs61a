ants.py: The game logic of Ants Vs. SomeBees
ants_gui.py: The original GUI for Ants Vs. SomeBees
gui.py: A new GUI for Ants Vs. SomeBees. Note that this doesn't work / is very buggy, but you can see the cute ants in motion here :)
graphics.py: Utilities for displaying simple two-dimensional animations
utils.py: Some functions to facilitate the game interface
ucb.py: Utility functions for CS 61A
state.py: Abstraction for gamestate for gui.py
assets: A directory of images and files used by gui.py
img: A directory of images used by ants_gui.py
ok: The autograder
proj3.ok: The ok configuration file
tests: A directory of tests used by ok

Rules: https://inst.eecs.berkeley.edu/~cs61a/fa20/proj/ants/

To Run this Game
python3 ants_gui.py

usage: ants_text.py [-h] [-d DIFFICULTY] [-w] [--food FOOD]

Play Ants vs. SomeBees

optional arguments:
  -h, --help     show this help message and exit
  -d DIFFICULTY  sets difficulty of game (test/easy/medium/hard/extra-hard)
  -w, --water    loads a full layout with water
  --food FOOD    number of food to start with when testing
