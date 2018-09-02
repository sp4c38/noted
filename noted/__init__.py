"""
The root module of the famous noted Python programm.
"""
import getpass
import os
import shutil
import sys

__version__ = '0.1.0'
__authors__ = ('Léon Becker <lb@space8.me')


def main():
    username = getpass.getuser()
    if os.path.isdir("/home/{}/.noted/saved_notes".format(username)):
        
        from noted import noted_edit_read
        from noted import noted_decrypt
        from noted import noted_delete 
        from noted import noted_normal_mode
        from noted import noted_project_mode
        from noted.prj_mode import prj_workon

        mode_selection = input("[1] normale mode [2] project mode [3] exit\n")
        if mode_selection in ("[1]", "1", "one"):
            print("\033[2J")
            print("\033[0;0H")
            noted_normal_mode.print_header()
            noted_normal_mode.main()
    
        elif mode_selection in ("[2]", "2", "two"):
            print("\033[2J")
            print("\033[0;0H")
            noted_project_mode.print_header()
            noted_project_mode.main()
        elif mode_selection in ("[3]", "3", "three"):
            print("Bye!")
            sys.exit(0)
    else:
        os.makedirs("/home/{}/.noted/saved_notes".format(username))
        main()
