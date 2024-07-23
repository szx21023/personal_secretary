from main import app

from .const import DailyEventStatus
from .model import DailyEvent

class DailyEventService:
    @staticmethod
    async def create_daily_event(event_name, event_type, **kargs):
        # if nether (both columns exist) nor (both columns not exist), raise error
        if not ((kargs.get('estimated_start_time') and kargs.get('estimated_end_time')) or \
        (not kargs.get('estimated_start_time') and not kargs.get('estimated_end_time'))):
            return

        if 'start_time' in kargs:
            kargs['status'] = DailyEventStatus.STARTED

        elif 'estimated_start_time' in kargs:
            kargs['status'] = DailyEventStatus.WAITING

        else:
            kargs['status'] = DailyEventStatus.IDLE

        kargs.update({
            'event_name': event_name,
            'event_type': event_type
        })
        daily_event = DailyEvent(**kargs)
        await daily_event.save()

    @staticmethod
    async def get_daily_event():
        daily_events = await DailyEvent.find().sort("-create_time").to_list()
        return daily_events