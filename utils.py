import base64

class InvalidDataException(Exception):
    pass

def text_decode(data):
    '''
        If data is in a text-encoded format return the decoded
        version, otherwise return data.

        NOTE: currently supporting base64 only
    '''
    if data.startswith("base64,"):
        split_data = data.split(',')

        # we expect split_data to be exactly 2, as 
        # b64-encoded data does not contain commas
        if len(split_data) != 2:
            raise InvalidDataException

        return base64.b64decode(split_data[1])

    else:
        return data
