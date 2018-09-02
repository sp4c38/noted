import os
import sys
import getpass
import shutil
import tempfile

from cryptography.fernet import Fernet

username = getpass.getuser()
saved_notes_location = (f"/home/{username}/.noted/saved_notes")

def main(note_selection=None, temp_file=None):
    
    with open(f"{saved_notes_location}/{note_selection}/file_txt.txt", "rb") as readfile_txt:
        readfile_txt = readfile_txt.read()

    with open(f"{saved_notes_location}/{note_selection}/file_key.txt", "rb") as readkey:
        readfile_key0 = readkey.read()
        readfile_key = Fernet(readfile_key0)

    decrypted_txt = (readfile_key.decrypt(readfile_txt))
    plaintext_decrypted_txt = bytes(decrypted_txt).decode("utf-8")

    temp_file.file.write(bytes(plaintext_decrypted_txt, 'utf-8'))
    temp_file.flush()