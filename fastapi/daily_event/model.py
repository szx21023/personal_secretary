from typing import Optional

from datetime import datetime
from pydantic import Field

from utils import InternalBaseDocument

class DailyEvent(InternalBaseDocument):
    event_name: str
    event_type: str
    estimated_start_time: datetime
    estimated_end_time: datetime

    description: Optional[str] = Field(None) # before daily_event
    note: Optional[str] = Field(None) # after daily_event
    start_time: Optional[datetime] = Field(None)
    end_time: Optional[datetime] = Field(None)
    cancel_time: Optional[datetime] = Field(None)

    class Settings:
        name = "daily_event"

    class Index:
        event_name_index = [("event_name", 1)]