import zipfile
import base64 
import io

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

        # simply store the data for later use
        self._data = data
        self._ctx = ctx
        self._output_dir = ctx['output_dir']

    def decode_data(self):
        '''
            Returns decoded data (to be used when data is not
            plain text but in a text-encoded format)
            
            NOTE: currently working with base64 only
        '''
        (encoder, data) = self._data.split(',')
        
        # For now we assume that encoder is always base64
        # and return the following:
        return base64.b64decode(data)

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
        if self._data.startswith("base64,"):
            self._data = self.decode_data().decode()


class ZipDataHandler(DataHandler):
    mime_type = "application/zip"

    def __init__(self, data, ctx):
        super().__init__(data, ctx)
        self._data = self.decode_data()

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
