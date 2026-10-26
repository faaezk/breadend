class BreadException(Exception):
    message = "Unknown Error"

    def __str__(self):
        return self.message

class UnknownException(BreadException):
    message = "Unknown Error"

class KeyException(BreadException):
    message = "Invalid parameters"

class NoneException(BreadException):
    message = "Insufficient Data"

class MissingException(BreadException):
    message = "Player not found"

class DynamicException(BreadException):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"{self.error_code}: {self.message}"
