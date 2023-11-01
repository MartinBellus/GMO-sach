class NetworkException(Exception):
    pass

class RemoteFileNotFound(Exception):
    pass

class InvalidGenomeException(Exception):
    pass


class OutOfCodons(InvalidGenomeException):
    pass