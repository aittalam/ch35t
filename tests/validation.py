import unittest
import json 
from jsonschema import validate, ValidationError
import os
from pathlib import Path

SCHEMA_VERSION = "1.0.0"
SCHEMA_FILE_PATH = Path(__file__).resolve().parent.parent / f"ch35t/schema/{SCHEMA_VERSION}.json"

class TestSchema(unittest.TestCase):
    
    good_files_path = "examples"
    bad_files_path = "tests/bad_json"
    
    def setUp(self):
        with open(SCHEMA_FILE_PATH, "rt") as f:
            self.s = json.load(f)
        
        self.good_files = [f for f in os.listdir(self.good_files_path)
                           if f.endswith("json")]
        self.bad_files = [f for f in os.listdir(self.bad_files_path) 
                          if f.endswith("json")]

    def load_and_validate(self, fname):
        with open(fname, "rt") as f:
            riddle = json.load(f)
        validate(schema=self.s, instance=riddle)
    
    def test_good_jsons(self):
        num_errors = 0
        for fname in [os.path.join(self.good_files_path, f) 
                      for f in self.good_files]:
            try:
                self.load_and_validate(fname)
            except ValidationError as e:
                print(f"ValidationError in {fname}: {e.message}")
                num_errors +=1

        if num_errors > 0:
            self.fail("Validation errors in good files - see below")

    def test_bad_jsons(self):
        for fname in [os.path.join(self.bad_files_path, f) 
                      for f in self.bad_files]:
            with self.assertRaises(ValidationError):
                self.load_and_validate(fname)
