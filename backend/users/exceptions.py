class NotFoundUser(Exception):
    pass


class UserHasAlreadyBeenCreated(Exception):
    pass


class BadRequest(Exception):
    pass


class IncorrectInfoForAuthenticateUser(Exception):
    pass


class TokenIsInvalid(Exception):
    pass


class TokenExpired(Exception):
    pass


class TokenNotHaveUserId(Exception):
    pass
