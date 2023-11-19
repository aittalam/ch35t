import hashlib

# application/octet-stream is used for generic binary files

class NullOutputDirException(Exception):
    pass


class MethodHandler:
    '''
        Handles payloads (depending on encryption method, it
        applies different algorithms to unlock a chest).
        Identified by its method (no two handlers
        have the same one).
    '''
    method = None

    def __init__(self, data, ctx):
        if ctx is None or ctx.get('output_dir', None) is None:
            raise NullOutputDirException

        # simply store the data for later use
        # (note that we assume data is already base64 decoded)
        self._data = data
        self._ctx = ctx
        self._output_dir = ctx['output_dir']
        self._cleartext_data = None

    def unlock(self, key):
        '''
            Unlocks a payload. This means applying an input key
            to the payload. The outcomes might differ (e.g. the
            key can be verified against a hash, it can be used
            to decrypt some content, etc.) but unlock is limited
            to verifying whether the key is correct and return
            True if so, False otherwise.
        '''
        raise NotImplementedError

class MD5Handler(MethodHandler):
    method = "md5"

    def unlock(self, key):
        '''
            Checks the key against a provided MD5 hash. Returns
            True if the hashed key matches, False otherwise
        '''

        if hashlib.md5(key.encode('utf-8')).hexdigest() == self._data:
            return True
        else:
            return False


# Dictionary mapping mime types to classes
handlers = {cls.method: cls for cls in MethodHandler.__subclasses__()}

def get_handler(method, data, ctx):
    if method in handlers:
        return handlers[method](data, ctx)
    else:
        raise ValueError(f"Unsupported method: {method}")
