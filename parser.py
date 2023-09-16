import hint
import payload
import json
import requests

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
            self._hint = hint.Hint(self._json)
            # load payload
            self._payload = payload.Payload(self._json)
    
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


### TODO: add some main code here showing how a parser works 