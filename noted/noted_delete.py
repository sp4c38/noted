import os
import shutil
import noted_normal_mode
import getpass

username = getpass.getuser()
saved_notes_location = (f"/home/{username}/.noted/saved_notes")

def main():
    saved_notes_list = os.listdir(saved_notes_location)
    if saved_notes_list:
        print("Your notes: ", ", ".join(saved_notes_list))
        delete_tree_ask = input("Which note do you want to delete?: ")
        if delete_tree_ask in saved_notes_list:
            shutil.rmtree(f"/home/{username}/.noted/saved_notes/{delete_tree_ask}")
            print(f"Succesfully deleted: {delete_tree_ask}")
                
            delete_tree_ask1 = input("\n[1] delete another note [2] return to main screen\n")
    
            if delete_tree_ask1 in ("[1]", "1", "one"):
                main()
            elif delete_tree_ask1 in ("[2]", "2", "two"):
                print()
                print("\033[2J")
                print("\033[0;0H")
                noted_normal_mode.main()
            else:
                print("Please only select \"1\" or \"2\"\n")
                main()
                    
        else:
            print("This note does not exist!")
            main()
    else:
        print("There are no saved notes!")
        noted_normal_mode.main()
