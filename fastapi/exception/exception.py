from fastapi import HTTPException
from fastapi import status


class InternalBaseException(HTTPException):
    def __init__(self, status_code: int = None, code: str = "ok", message: str = "success", **kwargs):
        detail = {
            "code": code,
            "message": message,
            "data": kwargs,
        }
        super().__init__(status_code=status_code, detail=detail)

class EstimatedTimeWrongValueException(InternalBaseException):
    code = "estimated_time_wrong_value"
    message = "estimated_start_time and estimated_end_time have wrong value"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)

class EventNameNotExistException(InternalBaseException):
    code = "event_name_not_exist"
    message = "Event_name does not exist"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)

class EventTypeIllegalException(InternalBaseException):
    code = "event_type_illegal"
    message = "Event_type is illegal"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)


