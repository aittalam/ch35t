import json
import requests

class NullHintException(Exception):
    pass

class NullPayloadException(Exception):
    pass

# application/octet-stream is used for generic files

# # Dictionary mapping mime types to functions
# handlers = {
#     "text/plain": handle_text,
#     "application/zip": handle_zip,
#     "image/svg+xml": handle_svg,
# }

# def process_data(data, mime_type):
#     if mime_type in handlers:
#         return handlers[mime_type](data)
#     else:
#         raise ValueError(f"Unsupported mime type: {mime_type}")

class ChestLoader():
    ### TODO: add error handling here
    def from_file(fname):
        with open(fname, "rt") as f:
            return json.load(f)
        
    def from_string(string):
        return json.loads(string)
    
    def from_url(url):
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text)


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
    
class Parser():

    def __init__(self, string=None):
        
        self._json = None
        self._hint = None
        self._payload = None
        self._method = None

        # If no string is provided as input, then the local json is uninitialized.
        # Note that it is possible to do so and manually load the json by calling 
        # one of the self._load_* methods defined before (dunno why yet, but I am
        # confident it might come useful at some point :-)
        if string is not None:
            if string.startswith("http://") or string.startswith("https://"):
                self._load_url(string)
            elif string.startswith("file://"):
                self._load_file(string[7:])
            else:
                self._load_string(string)
                
        if self._json is not None:
            # load hint
            self._hint = Hint(self._json)
            # load payload
            self._payload = Payload(self._json)
    
    def _load_string(self, string):
        self._json = ChestLoader.from_string(string)

    def _load_file(self, fname):
        self._json = ChestLoader.from_file(fname)
    
    def _load_url(self, url):
        self._json = ChestLoader.from_url(url)

    def json(self):
        return self._json

    def hint(self):
        return self._hint

    def payload(self):
        return self._payload