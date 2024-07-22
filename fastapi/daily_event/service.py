from main import app

from .model import DailyEvent

class DailyEventService:
    @staticmethod
    async def create_daily_event(event_name, event_type, estimated_start_time, estimated_end_time, **kargs):
        data = {
            'event_name': event_name,
            'event_type': event_type,
            'estimated_start_time': estimated_start_time,
            'estimated_end_time': estimated_end_time
        }
        daily_event = DailyEvent(**data)
        await daily_event.save()