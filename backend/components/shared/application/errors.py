from typing import Optional


class ApplicationError(RuntimeError):
    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message

    message = (
        "There was an unexpected application error,"
        " if this error persist contact support."
    )

    def __str__(self) -> str:
        return self.message


class UnknownMessageBusMessageType(ApplicationError):
    def __init__(self, message):
        self.message = f"{message} is not an Event or Command"
