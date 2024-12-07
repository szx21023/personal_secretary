from main import app
from exception.exception import EstimatedTimeWrongValueException, EventNameNotExistException, EventTypeIllegalException

from .const import DailyEventStatus, DailyEventType
from .model import DailyEvent
from .schema import DailyEventSchema

from customer.service import CustomerService

class DailyEventService:
    @staticmethod
    async def create_daily_event(customer_id, event_name, event_type, **kargs):
        customer = await CustomerService.get_customer_by_id(customer_id)

        # if nether (both columns exist) nor (both columns not exist), raise error
        if not ((kargs.get('estimated_start_time') and kargs.get('estimated_end_time')) or \
        (not kargs.get('estimated_start_time') and not kargs.get('estimated_end_time'))):
            exception = EstimatedTimeWrongValueException()
            app.logger.warning(exception.message)
            raise exception

        if not event_name:
            exception = EventNameNotExistException()
            app.logger.warning(exception.message)
            raise exception

        if event_type not in [member.value for _, member in DailyEventType.__members__.items()]:
            exception = EventTypeIllegalException()
            app.logger.warning(exception.message)
            raise exception

        if 'start_time' in kargs:
            kargs['status'] = DailyEventStatus.STARTED

        elif 'estimated_start_time' in kargs:
            kargs['status'] = DailyEventStatus.WAITING

        else:
            kargs['status'] = DailyEventStatus.IDLE

        kargs.update({
            'customer_id': customer_id,
            'event_name': event_name,
            'event_type': event_type
        })
        daily_event = DailyEvent(**kargs)
        await daily_event.save()

        schema = DailyEventSchema()
        daily_event = schema.dump(daily_event)
        return daily_event

    @staticmethod
    async def get_daily_event():
        daily_events = await DailyEvent.find().sort("-create_time").to_list()
        return daily_events