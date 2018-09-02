import os
import sys
import getpass
import shutil
from cryptography.fernet import Fernet

username = getpass.getuser()
saved_notes_location = (f"/home/{username}/.noted/saved_notes")

def main(str):
    
    with open(f"{saved_notes_location}/{str}/file_txt.txt", "rb") as readfile_txt:
        readfile_txt = readfile_txt.read()

    with open(f"{saved_notes_location}/{str}/file_key.txt", "rb") as readkey:
        readfile_key0 = readkey.read()
        readfile_key = Fernet(readfile_key0)

    decrypted_txt = (readfile_key.decrypt(readfile_txt))
    plaintext_decrypted_txt = bytes(decrypted_txt).decode("utf-8")
    
    note_selection_name = (f"{str}")
    saved_notes_edit_location = (f"/tmp/.noted/notes/{note_selection_name}")
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
    

    