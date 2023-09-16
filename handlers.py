# Dictionary mapping mime types to functions
handlers = {
    "text/plain": handle_text,
    "application/zip": handle_zip,
    "image/svg+xml": handle_svg,
}

def process_data(data, mime_type):
    if mime_type in handlers:
        return handlers[mime_type](data)
    else:
        raise ValueError(f"Unsupported mime type: {mime_type}")

class DataHandler():

    def __init__(self, data):
        pass

    def parse(self, data):
        pass

    def show():
        pass
