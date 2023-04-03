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
    message = "Something bad happened"
    def set_message(self, message):
        self.message = message
    pass