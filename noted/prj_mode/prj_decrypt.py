import os
import sys
import getpass
import tempfile
import shutil
from cryptography.fernet import Fernet

username = getpass.getuser()

def main(note_selection_decrypt=None, project_selection=None, temp_file=None):
    saved_notes_location = (f"/home/{username}/.noted/projects")
    with open(f"{saved_notes_location}/{project_selection}/{note_selection_decrypt}/file_txt.txt", "rb") as readfile_txt:
        readfile_txt = readfile_txt.read()

    with open(f"{saved_notes_location}/{project_selection}/{note_selection_decrypt}/file_key.txt", "rb") as readkey:
        readfile_key0 = readkey.read()
        readfile_key = Fernet(readfile_key0)

    decrypted_txt = (readfile_key.decrypt(readfile_txt))
    plaintext_decrypted_txt = bytes(decrypted_txt).decode("utf-8")

    # import IPython; IPython.embed()
    temp_file.file.write(bytes(plaintext_decrypted_txt, 'utf-8'))
    temp_file.file.flush()