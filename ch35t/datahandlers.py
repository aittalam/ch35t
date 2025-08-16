import zipfile
import io
from utils import text_decode

# application/octet-stream is used for generic binary files

class NullOutputDirException(Exception):
    pass

class DataHandler:
    '''
        Handles hints/payloads data so it can be easily accessed.
        Identified by its mime_type (no two handlers have the
        same one).
    '''
    mime_type = None

    def __init__(self, data, ctx):
        if ctx is None or ctx.get('output_dir', None) is None:
            raise NullOutputDirException

        # simply store text-decoded data for later use
        self._data = text_decode(data)
        self._ctx = ctx
        self._output_dir = ctx['output_dir']

    def to_string(self):
        '''
            Returns data (or a textual description of it) as a string
        '''
        return self._data

    def handle(self):
        '''
            
            (returns None)
        '''
        raise NotImplementedError


class TextDataHandler(DataHandler):
    mime_type = "text/plain"

    def __init__(self, data, ctx):
        super().__init__(data, ctx)

    def handle(self):
        # if data was base64-encoded, and after decoding it we have bytes,
        # we can assume text was encoded (e.g. in utf-8)
        # TODO: add support for different encodings, for now we only
        #       consider utf-8
        if type(self._data) == bytes:
            self._data = self._data.decode('utf-8')


class ZipDataHandler(DataHandler):
    mime_type = "application/zip"

    def __init__(self, data, ctx):
        super().__init__(data, ctx)

    def handle(self):
        with zipfile.ZipFile(io.BytesIO(self._data), "r") as zf:
            zf.extractall(self._output_dir)

    def to_string(self):
        s = f"Files are available in {self._output_dir}:\n"
        with zipfile.ZipFile(io.BytesIO(self._data), "r") as zf:
            for fileinfo in zf.infolist():
                s+=f"{fileinfo.filename}\n"
        return s

# Dictionary mapping mime types to classes
handlers = {cls.mime_type: cls for cls in DataHandler.__subclasses__()}

def get_handler(mime_type, data, ctx):
    if mime_type in handlers:
        return handlers[mime_type](data, ctx)
    else:
        raise ValueError(f"Unsupported mime type: {mime_type}")
