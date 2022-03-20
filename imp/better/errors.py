class BetterException(Exception):
    def __init__(self, message: str):
        self.message = message

class HostCheckError(BetterException):
    pass

class ParticipantCheckError(BetterException):
    pass

class GameCheckError(BetterException):
    pass

class PlayerTurnCheckError(BetterException):
    pass
