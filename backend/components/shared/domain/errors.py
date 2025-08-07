from typing import Optional

class DomainError(RuntimeError):
    message = (
        "There was an unexpected business error, if this error persist contact support."
    )

    def __str__(self) -> str:
        return self.message


class EntityNotFound(RuntimeError):
    entity = None

    def __init__(self, search_terms: dict):
        self.message = "Could not find {} with {}".format(self.entity, search_terms)

    def __str__(self) -> str:
        return self.message


class AuthorizationError(DomainError):
    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = "Forbidden"
