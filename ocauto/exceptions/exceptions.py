class BaseException(Exception):
    def __init__(self, message:str = None):
        self.message = message

class ScriptNotFoundError(BaseException):
    def __init__(self, message: str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return "{}".format("Script file not found.")
        return "{}".format(self.message)

class InvalidFileExtensionError(BaseException):
    def __init__(self, message: str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return "{}".format("Use of invalid file extension.")
        return "{}".format(self.message)

class TooManyParametersError(BaseException):
    def __init__(self, message: str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return "{}".format("The function supports only (1) parameter at a time.")
        return "{}".format(self.message)