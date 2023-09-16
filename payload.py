class NullPayloadException(Exception):
    pass

class Payload():
    _default_format = "text/plain"

    def __init__(self, json_data):
        payload = json_data.get('payload')
        if payload is None or (payload.get('data') is None and payload.get('origin') is None):
            raise NullPayloadException

        self.origin = payload.get('origin')
        self.data = payload.get('data')
        self.format = payload.get('format')
        self.method = payload.get('method')
        if self.format is None:
            self.format = self._default_format

    def __str__(self):
        return_str  =  "[i] Payload\n"
        return_str += f"    Origin: {self.origin}\n"
        return_str += f"    Data: {self.data}\n"
        return_str += f"    Format: {self.format}\n"
        return_str += f"    Method: {self.method}\n"
        return return_str
    
