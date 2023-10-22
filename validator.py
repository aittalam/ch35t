import json
import jsonschema

class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Validator():

    def __init__(self, schema_file="schema/1.0.0.json"):
        with open(schema_file, "rt") as f:
            self._schema = json.load(f)

    def validate(self, json):
        try:
            jsonschema.validate(schema=self._schema, instance=json)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)
