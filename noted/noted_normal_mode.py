import datetime
import getpass
import os
import shutil
import subprocess
import sys
from cryptography.fernet import Fernet

import noted
sys.path.append('prg_files/')
import noted_edit_read
import noted_decrypt
import noted_delete


username = getpass.getuser()
saved_notes_location = (f"/home/{username}/.noted/saved_notes/")
saved_notes_list = os.listdir(saved_notes_location)
# print("\033[2J")
# print("\033[0;0H")

def print_header():
    print("\033[2J")
    print("\033[0;0H")
    print("-- Noted -- v.1.0 (unreleased/in development)\n")


def get_editor(newnote_name):
    found_editor = False
    saved_notes_location = (f"/home/{username}/.noted/saved_notes/")

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
        run_editor = subprocess.run(f"{editor} /tmp/.noted/notes/{newnote_name}/{newnote_name}.txt",
        shell=True)

        with open(f"/tmp/.noted/notes/{newnote_name}/{newnote_name}.txt") as edited_file:
            edited_file = edited_file.read()

        newfile_encryption_key0 = Fernet.generate_key()
        newfile_encryption_key1 = Fernet(newfile_encryption_key0)
        newfile_encryption_txt = newfile_encryption_key1.encrypt(bytes(f"{edited_file}", "utf-8"))
        os.makedirs(f"{saved_notes_location}{newnote_name}")
        time_created = datetime.datetime.now().strftime("Created on: %m %d %Y, %H:%M")
        with open(f"{saved_notes_location}{newnote_name}/file_txt.txt", "wb") as file_object:
            file_object.write(newfile_encryption_txt)
        with open(f"{saved_notes_location}{newnote_name}/file_key.txt", "wb") as file_object:
            file_object.write(newfile_encryption_key0)
        with open (f"{saved_notes_location}{newnote_name}/metadata.txt", "w") as file_object:
            file_object.write(time_created)
        print("Note was created!")
        main()
    else:
        print("Did not find any 3rd-party editor to use! Please install vi, vim or set a enviroment variable to use your favourite editor!")

def main():
    saved_notes_list = os.listdir(saved_notes_location)
    if saved_notes_list:
        print("Your notes: ", ", ".join(saved_notes_list))
    else:
        print("No notes!")
    task_selection = input("[1] new note | [2] read/edit/save note| [3] delete note | [4] list notes | \n[5] back\n")

    def create_note():
            newnote_name = input("Name: ")
            if ' ' in newnote_name:
                print("The note name can not contain spaces!")
                create_note()

            if os.path.exists(f"/home/{username}/.noted/saved_notes/{newnote_name}"):
                print("This note name already exists!")
                create_note()
            else:
                if os.path.exists(f"/tmp/.noted/notes/{newnote_name}"):
                    with open(f"/tmp/.noted/notes/{newnote_name}/{newnote_name}.txt", "w") as file_object:
                        file_object.write("")
                    get_editor(newnote_name=newnote_name)
                else:
                    os.makedirs(f"/tmp/.noted/notes/{newnote_name}")
                    with open(f"/tmp/.noted/notes/{newnote_name}/{newnote_name}.txt", "w") as file_object:
                        file_object.write("")
                    get_editor(newnote_name=newnote_name)
                

    
    if task_selection in ("[1]", "1", "one"):
        print("\033[2J")
        print("\033[0;0H")
        print("Important: The note name can't contain spaces!")
        create_note()
    elif task_selection in ("[4]", "4", "four"):
        if saved_notes_list:
            print("\033[2J")
            print("\033[0;0H")
            print("Your notes: ", ", ".join(saved_notes_list))
            main()
        else:
            print("There are no saved notes!")
            main()
    elif task_selection in ("[3]", "3", "three"):
        noted_delete.main()

    elif task_selection in ("[2]", "2", "two"):
        noted_edit_read.main()
    elif task_selection in ("[5]", "5", "five"):
        print("\033[2J")
        print("\033[0;0H")
        noted.main()
    else:
        sys.exit(1)

if __name__ == '__main__':
    print_header()
    main()
