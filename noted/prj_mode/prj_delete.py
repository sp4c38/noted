import os
import shutil
import getpass

import prj_workon

username = getpass.getuser()

def main(str):
    project = str
    saved_notes_location = (f"/home/{username}/.noted/projects/{project}")
    saved_notes_list = os.listdir(saved_notes_location)
    if saved_notes_list:
        print("Your notes: ", ", ".join(saved_notes_list))
        delete_tree_ask = input("Which note do you want to delete?: ")
        if delete_tree_ask in saved_notes_list:
            shutil.rmtree(f"/home/{username}/.noted/projects/{project}/{delete_tree_ask}")
            print(f"Successfully deleted: {delete_tree_ask}")
                
            delete_tree_ask1 = input("\n[1] delete another note [2] return to main screen\n")
    
            if delete_tree_ask1 in ("[1]", "1", "one"):
                main(project)
            elif delete_tree_ask1 in ("[2]", "2", "two"):
                print("\033[2J")
                print("\033[0;0H")
                prj_workon.print_header()
                prj_workon.main(project)
            else:
                print("Please only select \"1\" or \"2\"!\n")
                main(project)
                    
        else:
            print("This note does not exist!")
            main(project)
    else:
        print("You have no notes!")
        print("\033[2J")
        print("\033[0;0H")
        prj_workon.print_header()
        prj_workon.main()
