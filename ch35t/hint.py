from ch35t.datahandlers import get_handler

class NullHintException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Hint():
    _default_format = "text/plain"

    def __init__(self, json_data):
        hint = json_data.get('hint')
        if hint is None or (hint.get('data') is None and hint.get('origin') is None):
            raise NullHintException("No hint has been provided in this chest's JSON")

        self.origin = hint.get('origin')
        self.data = hint.get('data')
        self.fmt = hint.get('format')
        if self.fmt is None:
            self.fmt = self._default_format
        self._datahandler = None

    def set_ctx(self, ctx):
        self._ctx = ctx

    def __str__(self):
        if self._datahandler is None:
            self._datahandler = get_handler(self.fmt, self.data, self._ctx)
            self._datahandler.handle()
        return self._datahandler.to_string()


    def dump(self):
        return_str  =  "[i] Hint\n"
        return_str += f"    Origin: {self.origin}\n"
        return_str += f"    Data: {self.data}\n"
        return_str += f"    Format: {self.fmt}\n"
        return return_str
