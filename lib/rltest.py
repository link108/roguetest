# Cameron Motevasselani

import argparse

from lib.main_menu import MainMenu

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="debug", action="store_true")
parser.add_argument("-g", "--god-mode", help="debug", action="store_true")

args = parser.parse_args()

main_menu = MainMenu(args)
main_menu.main_menu()
