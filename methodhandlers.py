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
        # simply store the data for later use
        # (note that we assume data is already base64 decoded)
        self._data = data
        self._ctx = ctx

    def unlock(self, key):
        '''
            
            (returns None)
        '''
        raise NotImplementedError


class MD5Handler(MethodHandler):
    method = "md5"

    def unlock(self, key):
        '''
            
            (returns None)
        '''

        if hashlib.md5(key.encode('utf-8')).hexdigest() == self._data:
            print("Chest unlocked")
        else:
            print("Wrong key")


# Dictionary mapping mime types to classes
handlers = {cls.method: cls for cls in MethodHandler.__subclasses__()}

def get_handler(method, data, ctx):
    if method in handlers:
        return handlers[method](data, ctx)
    else:
        raise ValueError(f"Unsupported method: {method}")
