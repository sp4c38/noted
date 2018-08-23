import datetime
import getpass
import os
import subprocess
import shutil
import sys
from cryptography.fernet import Fernet

import noted_project_mode
import prj_delete
import prj_workon
import prj_edit_read


username = getpass.getuser()
saved_notes_location = (f"/home/{username}/.noted/projects/")
# print("\033[2J")
# print("\033[0;0H")

def print_header():
    print("\033[2J")
    print("\033[0;0H")
    print("-- Noted -- v.1.0 (beta)\n")

def get_editor(newnote_name, project):
    found_editor = False
    saved_notes_location = (f"/home/{username}/.noted/projects/{project}/")

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
        run_editor = subprocess.run(f"{editor} /tmp/.noted/projects/{project}/{newnote_name}/{newnote_name}.txt",
        shell=True)

        with open(f"/tmp/.noted/projects/{project}/{newnote_name}/{newnote_name}.txt") as edited_file:
            edited_file = edited_file.read()

        newfile_encryption_key0 = Fernet.generate_key()
        newfile_encryption_key1 = Fernet(newfile_encryption_key0)
        newfile_encryption_txt = newfile_encryption_key1.encrypt(bytes(f"{edited_file}", "utf-8"))
        os.makedirs(f"{saved_notes_location}{newnote_name}")
        time_created = datetime.datetime.now().strftime("%m %d %Y, %H:%M")
        with open(f"{saved_notes_location}{newnote_name}/file_txt.txt", "wb") as file_object:
            file_object.write(newfile_encryption_txt)
        with open(f"{saved_notes_location}{newnote_name}/file_key.txt", "wb") as file_object:
            file_object.write(newfile_encryption_key0)
        with open (f"{saved_notes_location}{newnote_name}/metadata.txt", "w") as file_object:
            file_object.write(time_created)
        print("Note was created!")
        main(project)
    else:
        print("Did not find any 3rd-party editor to use! Please install vi, vim or set a enviroment variable to use your favourite editor!")


def main(str):
    project = str
    saved_notes_list = os.listdir(f"{saved_notes_location}{project}")
    if saved_notes_list:
        print("Your notes: ", ", ".join(saved_notes_list))
    else:
        print("No notes!")
    task_selection = input("[1] new note | [2] read/edit note | [3] delete note "
        "\n[4] list notes | [5] back \n")

    def create_note():
            newnote_name = input("Name: ")
            if ' ' in newnote_name:
                print("The note name can not contain any spaces!")
                create_note()

            if os.path.exists(f"/home/{username}/.noted/projects/{project}/{newnote_name}"):
                print("This note name already exists!")
                create_note()
            else:
                if os.path.exists(f"/tmp/.noted/projects/{project}/{newnote_name}"):
                    with open(f"/tmp/.noted/projects/{project}/{newnote_name}/{newnote_name}.txt", "w") as file_object:
                        file_object.write("")
                    get_editor(newnote_name=newnote_name, project=project)
                else:
                    os.makedirs(f"/tmp/.noted/projects/{project}/{newnote_name}")
                    with open(f"/tmp/.noted/projects/{project}/{newnote_name}/{newnote_name}.txt", "w") as file_object:
                        file_object.write("")
                    get_editor(newnote_name=newnote_name, project=project)

    
    if task_selection in ("[1]", "1", "one"):
        print("\033[2J")
        print("\033[0;0H")
        print("Important: The note name can't contain spaces!")
        create_note()
    elif task_selection in ("[4]", "4", "four"):
        saved_notes_list = os.listdir(f"{saved_notes_location}{project}")
        if saved_notes_list:
            print("\033[2J")
            print("\033[0;0H")
            main(project)
        else:
            print("You do not have any notes!")
            main(project)
    elif task_selection in ("[3]", "3", "three"):
        prj_delete.main(project)

    elif task_selection in ("[2]", "2", "two"):
        prj_edit_read.main(project)
    elif task_selection in ("[5]", "5", "five"):
        print("\033[2J")
        print("\033[0;0H")
        noted_project_mode.main()
    else:
        sys.exit(1)

if __name__ == '__main__':
    print_header()
    main()
