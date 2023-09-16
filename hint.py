class NullHintException(Exception):
    pass
 
class Hint():
    _default_format = "text/plain"

    def __init__(self, json_data):
        hint = json_data.get('hint')
        if hint is None or (hint.get('data') is None and hint.get('origin') is None):
            raise NullHintException

        self.origin = hint.get('origin')
        self.data = hint.get('data')
        self.format = hint.get('format')
        if self.format is None:
            self.format = self._default_format

    def __str__(self):
        return_str  =  "[i] Hint\n"
        return_str += f"    Origin: {self.origin}\n"
        return_str += f"    Data: {self.data}\n"
        return_str += f"    Format: {self.format}\n"
        return return_str

