import json
import requests
import hashlib
import zipfile
import base64
import os

import parser
import datahandlers
import methodhandlers

class Chest():
    def __init__(self, chestfile, chests_dir="/tmp/chests"):
        self._chests_dir = chests_dir
        self._parser = parser.Parser(chestfile)
        self._hint = self._parser.hint()
        self._payload = self._parser.payload()
        self._ctx = { "output_dir": chests_dir }
        
        if not os.path.exists(chests_dir):
            print(f"[i] Creating chests directory {chests_dir}")
            os.mkdir(chests_dir)
        
    def show_hint(self):
        h = datahandlers.get_handler(self._hint.format, self._hint.data, self._ctx)
        h.handle()
        print(h.to_string())
                
    def unlock(self):
        key = input()

        h = methodhandlers.get_handler(self._payload.method, self._payload.data, self._ctx)
        h.unlock(key)
