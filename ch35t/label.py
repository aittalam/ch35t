class NullLabelException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Label():

    def __init__(self, json_data):
        label = json_data.get('label')
        if label is None or label.get('name') is None:
            raise NullLabelException("No valid label has been provided in this chest's JSON")

        self.name = label.get('name')
        self.author = label.get('author')
        self.URI = label.get('URI')


    def dump(self):
        return_str  =  "[i] Label\n"
        return_str += f"    Name: {self.name}\n"
        return_str += f"    Author: {self.author}\n"
        return_str += f"    URI: {self.URI}\n"
        return return_str
