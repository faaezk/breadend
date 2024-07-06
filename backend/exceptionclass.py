class UnknownException(Exception):
    message = "Unknown Error"
    pass

class KeyException(Exception):
    message = "Invalid parameters"
    pass

class NoneException(Exception):
    message = "Insufficient Data"
    pass

class MissingException(Exception):
    message = "Player not found"
    pass

class DynamicException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"{self.error_code}: {self.message}"
    pass