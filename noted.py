import getpass
import os
import shutil
import sys
from cryptography.fernet import Fernet


username = getpass.getuser()


def main():
    if os.path.isdir("/home/{}/.noted/saved_notes".format(username)):
        sys.path.append('prg_files/')
        
        import noted_edit_read
        import noted_decrypt
        import noted_delete 
        import noted_normal_mode
        import noted_project_mode
        sys.path.append('prg_files/prj_mode')
        import prj_workon

        mode_selection = input("[1] normale mode [2] project mode [3] exit\n")
        if mode_selection in ("[1]", "1", "one"):
            print("\033[2J")
            print("\033[0;0H")
            noted_normal_mode.print_header()
            noted_normal_mode.main()
    
        elif mode_selection in ("[2]", "2", "two"):
            print("\033[2J")
            print("\033[0;0H")
            noted_project_mode.main()
        elif mode_selection in ("[3]", "3", "three"):
            print("Bye!")
            sys.exit(0)
    else:
        os.makedirs("/home/{}/.noted/saved_notes".format(username))
        main()

if __name__ == '__main__':
    main()
