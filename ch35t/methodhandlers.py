import os
import base64
import hashlib
from .utils import text_decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class NullOutputDirException(Exception):
    pass

class MethodHandler:
    '''
        Handles payloads (depending on encryption method, it
        applies different algorithms to unlock/lock a chest).
        Identified by its method (no two handlers
        have the same one).
    '''
    method = None

    def __init__(self, data, ctx):
        if ctx is None or ctx.get('output_dir', None) is None:
            raise NullOutputDirException

        # simply store data for later use
        self._data = data
        self._ctx = ctx
        self._output_dir = ctx['output_dir']
        self._cleartext_data = None

    def lock(self, key):
        '''
            Applies a cryptographic algorithm to lock self._data with the
            provided key.
            Regardless of the employed algorithm, locking should always
            return the encrypted data as a string (possibly base64-encoded)
        '''
        raise NotImplementedError

    def unlock(self, key):
        '''
            Applies a cryptographic algorithm to unlock self._data with the
            provided key.
            "Unlocking" has different outcomes depending on the algorithm
            (e.g. the key can be verified against a hash, used to decrypt 
            some content, etc.).

            After unlocking, this function does the following:
            - update self._cleartext_data if any data is generated
              (dealing with cleartext data is a task for payload class)
            - return True if the key was correct, False otherwise
        '''
        raise NotImplementedError


class MD5Handler(MethodHandler):
    method = "md5"

    def lock(self):
        '''
            Returns the MD5 hash of self._data
        '''

        return hashlib.md5(self._data.encode('utf-8')).hexdigest()

    def unlock(self, key):
        '''
            Checks the key against a provided MD5 hash. Returns
            True if the hashed key matches, False otherwise
        '''

        # base64 is probably never used together with MD5...
        # but who knows :-)
        self._data = text_decode(self._data)
        if hashlib.md5(key.encode('utf-8')).hexdigest() == self._data:
            return True
        else:
            return False


class AESHandler(MethodHandler):
    method = "AES"

    def _get_cipher(self, key, iv=None):
        '''
            Given a key and an optional initialization vector,
            returns an AES cipher object that can be used
            both for encryption and decryption.

            For encryption, it is suggested to always use random
            ivs (if none is passed to the function, a random one
            will be created)
        '''

        # to have consistent, 32-bytes key length,
        # the key is converted into its md5 hash
        key = bytes(hashlib.md5(bytes(key, 'utf-8')).hexdigest(), 'utf-8')

        if iv is None:
            # set the initialization vector to 16 random bytes
            iv = os.urandom(16)

        # create an AES encryptor object
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

        return cipher, iv

    def lock(self, key):
        '''
            Given a key, encrypts data using the AES algorithm.
            Data is returned as base64-encoded so it can be easily
            handled in ch35t json files.
        '''
        cipher, iv = self._get_cipher(key)
        encryptor = cipher.encryptor()

        # encrypt
        ct = encryptor.update(bytes(self._data, 'utf-8')) + encryptor.finalize()

        # concatenate iv and ct
        full_message = bytearray(iv)
        full_message.extend(ct)
        full_message = base64.b64encode(full_message).decode('utf-8')

        # update self._data
        return f"base64,{full_message}"

    def unlock(self, key):
        '''
            Given a key, decrypts data using the AES algorithm.
            If decrypted data is not junk (i.e. utf-8 decoding
            does not break), it returns True and saves it as
            cleartext_data, otherwise it returns False
        '''

        # data is provided as base64-encoded, so decode it first
        data = text_decode(self._data)

        # recover iv and ct from data
        iv = data[:16]
        ct = data[16:]

        cipher,_ = self._get_cipher(key, iv)
        decryptor = cipher.decryptor()

        # decrypt
        pt = decryptor.update(ct) + decryptor.finalize()

        # we have no real way to know whether the key is correct
        # as AES will decrypt in any case, but if what is returned
        # is garbage the utf-8 decoding will break
        try:
            pt = pt.decode('utf-8')
        except UnicodeDecodeError as e:
            return False

        self._cleartext_data = pt
        return True


# Dictionary mapping mime types to classes
handlers = {cls.method: cls for cls in MethodHandler.__subclasses__()}

def get_handler(method, data, ctx):
    if method in handlers:
        return handlers[method](data, ctx)
    else:
        raise ValueError(f"Unsupported method: {method}")
