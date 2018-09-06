from cryptography.fernet import Fernet
import datetime
import getpass
import os
import subprocess
import shutil
import sys
import tempfile

from . import noted_normal_mode
from . import noted_decrypt

username = getpass.getuser()
saved_notes_location = (f"/home/{username}/.noted/saved_notes")
note_selection = ("")


def get_editor():

    with tempfile.TemporaryDirectory() as tempdir:

        temp_file = tempfile.NamedTemporaryFile(dir=f'{tempdir}/', prefix='noted_')
        noted_decrypt.main(note_selection=note_selection, temp_file=temp_file)
        found_editor = False

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
            run_editor = subprocess.run(f"{editor} {temp_file.name}", shell=True)

            with open(f"{temp_file.name}") as edited_file:
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
            with open(f"{saved_notes_location}/{note_selection}/metadata.txt", "w") as metadate_write:
                metadate_write.write(f"Last time edited: {time_created}")

            print("\033[2J")
            print("\033[0;0H")
            print("Successfully edited!")
            noted_normal_mode.main()

        else:
            print("Did not find any editor! Please install vi, vim, subl (SublimeText) or nano")



def main():
    global note_selection
    saved_notes_list = os.listdir(saved_notes_location)
    if saved_notes_list: 
        print("Your notes: ", ", ".join(saved_notes_list))
        note_selection = input("Which note do you want to read/edit/save: ")

        if note_selection in saved_notes_list:
            
            ask_selection = input("[r]ead | [e]dit | [s]ave\nSelect option: ")

            if ask_selection.lower() in ("[r]", "read", "r"):
                print("\033[2J")
                print("\033[0;0H")
                with open(f"/home/{username}/.noted/saved_notes/{note_selection}/metadata.txt") as file_read:
                    print(file_read.read())

                with tempfile.TemporaryDirectory() as tempdir:
                    temp_file = tempfile.NamedTemporaryFile(dir=f'{tempdir}/', prefix='noted_')
                    
                    noted_decrypt.main(note_selection=note_selection, temp_file=temp_file)
                    with open(temp_file.name) as read_file:
                        print("\n-- BEGINNING --\n", read_file.read(), "-- END --\n")
                    noted_normal_mode.main()
                    

            elif ask_selection.lower() in ("[e]", "edit", "e"):
                get_editor()
            elif ask_selection.lower() in ("[s]", "save", "s"):
                save_path = input("Please specify where to save your note (e.g. /home/<username>/Downloads):\n")
                if os.path.isdir(save_path):
                    with tempfile.TemporaryDirectory() as tempdir:
                        temp_file = tempfile.NamedTemporaryFile(dir=f'{tempdir}/', prefix='noted_')
                        noted_decrypt.main(note_selection=note_selection, temp_file=temp_file)
                        shutil.move(os.path.join(temp_file.name),
                            os.path.join(save_path, f"{note_selection}.txt"))

                    noted_normal_mode.print_header()
                    print(f"File: {note_selection}.txt, was successfully copied to {save_path}")
                    noted_normal_mode.main()
                else:
                    print("This path doesn't exist!")
                    noted_normal_mode()
            else:
                print("Error: Option not found!")
                    

        else:
            print(f"--> The note \"{note_selection}\" does not exist!\n")
            main()

    else:
        print("You do not have any saved notes!")
        
