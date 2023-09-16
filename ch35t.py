import json
import requests
import hashlib
import zipfile
import base64
import os

import parser

# application/octet-stream is used for generic files


class Chest():
    def __init__(self, chestfile, chests_dir="/tmp/chests"):
        self._parser = parser.Parser(chestfile)
        self._hint = self._parser.hint()
        self._payload = self._parser.payload()

        if not os.path.exists(chests_dir):
            print(f"[i] Creating chests directory {chests_dir}")
            os.mkdir(chests_dir)
        
    def show_hint(self):
        if self._hint.format == 'text/plain':
            print(self._hint.data)
        # elif self._hint.format == 'application/zip':
        #     # base64-decode it
        #     # unzip it
        #     with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        #     # show directory content
                
    def unlock(self):
        key = input()

        # get data
        ### TODO: add other means to get data depending on data type
        ### (this should be done in parser, not here)
        if self._payload.format == 'text/plain':
            data = self._payload.data
            
        if self._payload.method == 'md5':
            if hashlib.md5(key.encode('utf-8')).hexdigest() == data:
                print("Yay, you got the right password!")
            else:
                print("Nay, this is the wrong one!")

