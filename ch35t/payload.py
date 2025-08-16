import ch35t.methodhandlers as mh
import ch35t.datahandlers as dh

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
        self.cleartext_data = None
        self._methodhandler = None
        self._datahandler = None

        # if a method is specified (note that it is optional!), get its name
        self.method = None
        m = payload.get('method')
        if m is not None:
            self.method = m.get('name')
 
        if self.fmt is None:
            self.fmt = self._default_format

    def set_ctx(self, ctx):
        self._ctx = ctx

    def unlock(self, key):
        # calls methodhandler to unlock the payload
        if self._methodhandler is None:
            self._methodhandler = mh.get_handler(self.method, self.data, self._ctx)

        if self._methodhandler.unlock(key):
            self.cleartext_data = self._methodhandler._cleartext_data
            return True

        return False

    def __str__(self):
        if self._datahandler is None:
            if not self.cleartext_data:
                ctdata = self.data

            if hasattr(self, "_ctx"):
                context = self._ctx
            else:
                context = {"output_dir": "/tmp"}

            self._datahandler = dh.get_handler(self.fmt, ctdata, context)
            self._datahandler.handle()

        return self._datahandler.to_string()

    def dump(self):
        return_str  =  "[i] Payload\n"
        return_str += f"    Origin: {self.origin}\n"
        return_str += f"    Data: {self.data}\n"
        return_str += f"    Cleartext Data: {self.cleartext_data}\n"
        return_str += f"    Format: {self.fmt}\n"
        return_str += f"    Method: {self.method}\n"
        return return_str
    
