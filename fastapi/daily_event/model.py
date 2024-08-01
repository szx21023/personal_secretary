from typing import Optional

from datetime import datetime
from pydantic import Field

from utils import InternalBaseDocument

class DailyEvent(InternalBaseDocument):
    event_name: str
    event_type: str
    status: str

    description: Optional[str] = Field(None) # before daily_event
    note: Optional[str] = Field(None) # after daily_event
    estimated_start_time: Optional[datetime] = Field(None)
    estimated_end_time: Optional[datetime] = Field(None)
    start_time: Optional[datetime] = Field(None)
    end_time: Optional[datetime] = Field(None)
    cancel_time: Optional[datetime] = Field(None)

    class Settings:
        name = "daily_event"