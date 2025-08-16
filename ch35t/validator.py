import json
import jsonschema
from pathlib import Path

SCHEMA_VERSION = "1.0.0"
SCHEMA_FILE_PATH = Path(__file__).resolve().parent / f"schema/{SCHEMA_VERSION}.json"

class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Validator():

    def __init__(self, schema_file=SCHEMA_FILE_PATH):
        with open(schema_file, "rt") as f:
            self._schema = json.load(f)

    def validate(self, json):
        try:
            jsonschema.validate(schema=self._schema, instance=json)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)
