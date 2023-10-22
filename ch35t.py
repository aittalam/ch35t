import json
import requests
import hashlib
import zipfile
import base64
import os

import parser
import validator

class Chest():
    def __init__(self, chestfile, chests_dir="/tmp/chests"):
        self._chests_dir = chests_dir
        self._parser = parser.Parser(chestfile)
        self.hint = self._parser.hint()
        self.payload = self._parser.payload()
        self.label = self._parser.label()
        self._validator = validator.Validator()
        self._ctx = {
            "output_dir": chests_dir
        }
        
        if not os.path.exists(chests_dir):
            print(f"[i] Creating chests directory {chests_dir}")
            os.mkdir(chests_dir)

        # set context for hint and payload
        # Hint and payload might be null if there is a parsing
        # error OR if the parser has been explicitly initialized
        # with no JSON, for later manual loading (we should make
        # manual loading available to this class and the CLI too!)
        if self.hint is not None:
            self.hint.set_ctx(self._ctx)
        if self.payload is not None:
            self.payload.set_ctx(self._ctx)

    def unlock(self, key):
        # try to unlock the chest, if successful return True
        return self.payload.unlock(key)

    def json(self):
        return self._parser.json()

    def validate(self):
        self._validator.validate(self.json())

    def name(self):
        return self.label.name

    def author(self):
        return self.label.author
