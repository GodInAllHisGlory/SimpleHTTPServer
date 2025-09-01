class Request:
    def __init__(
        self,
        method, #string
        uri, #string
        version, #string
        body, #string
        headers, #dict, the keys are the header names and values are the header values
    ):
        self.method = method
        self.uri = uri
        self.version = version
        self.body = body
        self.headers = headers