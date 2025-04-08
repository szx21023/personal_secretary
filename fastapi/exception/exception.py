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

class EventStatusNotWaitingException(InternalBaseException):
    code = "event_status_not_waiting"
    message = "Event_status is not waiting"

    def __init__(self, message: str = None, daily_event = None, **kwargs):
        _message = message or self.message
        if daily_event:
            _message = f"{_message}, daily_event: {str(daily_event.id)}"
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)

class EventTypeIllegalException(InternalBaseException):
    code = "event_type_illegal"
    message = "Event_type is illegal"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)

class EventAlreadyExistAtSameTimeException(InternalBaseException):
    code = "event_already_exist_at_same_time"
    message = "Event already exist at same time"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)

class CustomerNotExistException(InternalBaseException):
    code = "customer_not_exist"
    message = "customer not exist"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_404_NOT_FOUND, self.code, _message, **kwargs)

class CustomerCreatedFailException(InternalBaseException):
    code = "customer_created_fail"
    message = "customer created fail"

    def __init__(self, message: str = None, **kwargs):
        _message = message or self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)
