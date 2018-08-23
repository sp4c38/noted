import os
import sys
import getpass
import shutil
from cryptography.fernet import Fernet

username = getpass.getuser()

def main(note_selection_decrypt=None, project_selection=None):
    saved_notes_location = (f"/home/{username}/.noted/projects")
    with open(f"{saved_notes_location}/{project_selection}/{note_selection_decrypt}/file_txt.txt", "rb") as readfile_txt:
        readfile_txt = readfile_txt.read()

    with open(f"{saved_notes_location}/{project_selection}/{note_selection_decrypt}/file_key.txt", "rb") as readkey:
        readfile_key0 = readkey.read()
        readfile_key = Fernet(readfile_key0)

    decrypted_txt = (readfile_key.decrypt(readfile_txt))
    plaintext_decrypted_txt = bytes(decrypted_txt).decode("utf-8")
    
    note_selection_name = (f"{note_selection_decrypt}")
    saved_notes_edit_location = (f"/tmp/.noted/projects/{project_selection}/{note_selection_name}")
    saved_notes_edit_location_txt = (f"{saved_notes_edit_location}/{note_selection_name}.txt")

    if os.path.isdir(saved_notes_edit_location):
        shutil.rmtree(saved_notes_edit_location)
        os.makedirs(saved_notes_edit_location)  
        with open(saved_notes_edit_location_txt, "w") as writefile:
            writefile.write(plaintext_decrypted_txt)
            
    else:
        os.makedirs(saved_notes_edit_location)  
        with open(saved_notes_edit_location_txt, "w") as writefile:
            writefile.write(plaintext_decrypted_txt)

    

    