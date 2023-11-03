class InvalidUserIdKey(KeyError):
    "Raised when there is no UserID in the Stack response"
    pass

class InvalidDisplayNameKey(KeyError):
    "Raised when there is no DisplayName in the Stack response"
    pass

class UnsuccessfulDBSave(Exception):
    "Raised when there is an unsuccessful save to the DB"
    pass