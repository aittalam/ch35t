from ch35t.hint import Hint
from ch35t.payload import Payload
from ch35t.label import Label
import json
import requests


class ParserException(Exception):
        def __init__(self, message):
                    super().__init__(message)


class ChestLoader():
    ### TODO: add better error handling here
    def from_file(fname):
        try:
            with open(fname, "rt") as f:
                return json.load(f)
        except Exception as e:
            raise ParserException(e)
        
    def from_string(string):
        try:
            return json.loads(string)
        except Exception as e:
            raise ParserException(e)
    
    def from_url(url):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return json.loads(res.text)
            return None
        except Exception as e:
            raise ParserException(e)


class Parser():

    def __init__(self, string=None):
        
        self._json = None
        self._hint = None
        self._label = None
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
                
        # JSON is parsed only if not null
        # This is done to allow for later manual loading of JSON,
        # or to take JSON parsing errors into account
        if self._json is not None:
            self._parse_json()
    
    def _load_string(self, string):
        self._json = ChestLoader.from_string(string)

    def _load_file(self, fname):
        self._json = ChestLoader.from_file(fname)
    
    def _load_url(self, url):
        self._json = ChestLoader.from_url(url)

    def _parse_json(self):
        self._hint = Hint(self._json)
        self._payload = Payload(self._json)
        self._label = Label(self._json)

    def json(self):
        return self._json

    def hint(self):
        return self._hint

    def payload(self):
        return self._payload

    def label(self):
        return self._label

### TODO: add some main code here showing how a parser works
