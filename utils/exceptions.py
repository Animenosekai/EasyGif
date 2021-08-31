from utils.log import LogLevels, log

class EasyGifException(Exception):
    SAFE_MESSAGE = "{mention} ❌ An error occured while processing your request"
    def __init__(self, message: str, *args: object) -> None:
        log(message, level=LogLevels.ERROR)
        super().__init__(*args)

class WrongProvider(EasyGifException):
    SAFE_MESSAGE = "{mention} ❌ An error occured while processing your request (error: WRONG_PROVIDER)"
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)

class RequestError(EasyGifException):
    SAFE_MESSAGE = "{mention} ❌ An error occured while making a request to process your request"
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)

class NoResult(EasyGifException):
    SAFE_MESSAGE = "{mention} ❌ We couldn't find any result"
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)

class MessageNotFound(EasyGifException):
    SAFE_MESSAGE = "{mention} ❌ You are not on the right channel or we could not find the last GIF sent"
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)