from cryptography.fernet import Fernet
import datetime
import getpass
import os
import subprocess
import shutil
import sys
import prj_workon
import prj_decrypt

username = getpass.getuser()
note_selection = ("")


def get_editor(project_selection):
    found_editor = False
    saved_notes_location = (f"/home/{username}/.noted/projects/{project_selection}")

    possible_editors = ('vim', 'vi', 'subl', 'nano')

    for e in possible_editors:
        try:
            subprocess.check_call(['which', e])
        except subprocess.CalledProcessError as exec:
            continue
        print("Using {} as the editor".format(e))
        found_editor = True
        editor = e
        break

    if editor.endswith('subl'):
        editor += ' --wait'

    if found_editor == True:
        run_editor = subprocess.run(f"{editor} /tmp/.noted/projects/{project_selection}/{note_selection}/{note_selection}.txt",
        shell=True)

        with open(f"/tmp/.noted/projects/{project_selection}/{note_selection}/{note_selection}.txt") as edited_file:
            edited_file = edited_file.read()

        newfile_encryption_key0 = Fernet.generate_key()
        newfile_encryption_key1 = Fernet(newfile_encryption_key0)
        newfile_encryption_txt = newfile_encryption_key1.encrypt(bytes(f"{edited_file}", "utf-8"))
        shutil.rmtree(f"{saved_notes_location}/{note_selection}")
        os.makedirs(f"{saved_notes_location}/{note_selection}")
        time_created = datetime.datetime.now().strftime("%m %d %Y, %H:%M")
        
        with open(f"{saved_notes_location}/{note_selection}/file_txt.txt", "wb") as file_object:
            file_object.write(newfile_encryption_txt)
        with open(f"{saved_notes_location}/{note_selection}/file_key.txt", "wb") as file_object:
            file_object.write(newfile_encryption_key0)
        with open(f"{saved_notes_location}/{note_selection}/metadata.txt", "w") as file_object:
            file_object.write(f"Last time edited: {time_created}")

        print("\033[2J")
        print("\033[0;0H")
        print("Successfully edited!")
        prj_workon.main(project_selection)

    else:
        print("Did not find any 3rd-party editor to use! Please install vi, vim or set a enviroment variable to use your favourite editor!")



def main(str):
    project = str
    saved_notes_location = (f"/home/{username}/.noted/projects/{project}/")
    global note_selection
    saved_notes_list = os.listdir(saved_notes_location)
    if saved_notes_list: 
        print("Your notes: ", ", ".join(saved_notes_list))
        note_selection = input("Which note do you want to read/edit/save: ")

        if note_selection in saved_notes_list:
            
            prj_decrypt.main(note_selection_decrypt=note_selection, project_selection=project)

            ask_selection = input("[r]ead | [e]dit | [s]ave\nSelect option: ")

            if ask_selection.lower() in ("[r]", "read", "r"):
                print("\033[2J")
                print("\033[0;0H")

                with open(f"/home/{username}/.noted/projects/{project}/{note_selection}/metadata.txt") as read_file:
                    print(read_file.read())
                with open(f"/tmp/.noted/projects/{project}/{note_selection}/{note_selection}.txt") as read_file:
                    print("-- BEGINNING --\n", read_file.read(), "\n-- END --\n")
                prj_workon.main(project)
                    
            elif ask_selection.lower() in ("[e]", "edit", "e"):
                get_editor(project_selection=project)
            elif ask_selection.lower() in ("[s]", "save", "s"):
                save_path = input("Please specify where to save your note (e.g. /home/<username>/Downloads):\n")
                if os.path.isdir(save_path):
                    shutil.move(os.path.join(f"/tmp/.noted/projects/{project}/{note_selection}/{note_selection}.txt"),
                        os.path.join(save_path, f"{note_selection}.txt"))

                    prj_workon.print_header()
                    print(f"File: {note_selection}.txt, was successfully copied to {save_path}")
                    prj_workon.main(project)
                else:
                    print("This path doesn't exist!")
                    prj_workon(project)
            else:
                print("Error: Option not found!")
                    

        else:
            print(f"--> The note \"{note_selection}\" does not exist!\n")
            main(project)

    else:
        print("\033[2J")
        print("\033[0;0H")
        print("You do not have any notes!")
        prj_workon.main(project)
        
