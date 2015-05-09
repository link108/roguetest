# Cameron Motevasselani

import argparse

from lib.main_menu import MainMenu

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="debug")

args = parser.parse_args()

main_menu = MainMenu(args)
main_menu.main_menu()
