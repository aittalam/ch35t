class NullPayloadException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Payload():
    _default_format = "text/plain"

    def __init__(self, json_data):
        payload = json_data.get('payload')
        if payload is None or (payload.get('data') is None and payload.get('origin') is None):
            raise NullPayloadException("No payload has been provided in this chest's JSON")

        self.origin = payload.get('origin')
        self.data = payload.get('data')
        self.fmt = payload.get('format')

        # if a method is specified (note that it is optional!), get its name
        self.method = None
        m = payload.get('method')
        if m is not None:
            self.method = m.get('name')
 
        if self.fmt is None:
            self.fmt = self._default_format


    def set_ctx(self, ctx):
        self._ctx = ctx


    def dump(self):
        return_str  =  "[i] Payload\n"
        return_str += f"    Origin: {self.origin}\n"
        return_str += f"    Data: {self.data}\n"
        return_str += f"    Format: {self.fmt}\n"
        return_str += f"    Method: {self.method}\n"
        return return_str
    
