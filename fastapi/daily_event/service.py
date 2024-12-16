from main import app
from exception.exception import EstimatedTimeWrongValueException, EventNameNotExistException, EventTypeIllegalException

from .const import DailyEventStatus, DailyEventType
from .model import DailyEvent
from .schema import DailyEventSchema

from customer.service import CustomerService
from utils import system_tz

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

        await DailyEventService.setup_schedule_remind(daily_event)
        schema = DailyEventSchema()
        daily_event = schema.dump(daily_event)
        return daily_event

    @staticmethod
    async def get_daily_event():
        daily_events = await DailyEvent.find().sort("-create_time").to_list()
        return daily_events

    @staticmethod
    async def setup_schedule_remind(daily_event):
        from line.service import LineService

        if daily_event.status == DailyEventStatus.WAITING:
            job_id = f'job_remind_coming_daily_event_{str(daily_event.id)}'
            run_date = daily_event.estimated_start_time.replace(tzinfo=system_tz())
            job = app.scheduler.add_job(LineService.remind_coming_daily_event, 'date', run_date=run_date, id=job_id, args=[daily_event])
            message = f"setup job_remind_coming_daily_event, job_id: {job_id}, run_date: {run_date}"
            app.logger.info(message)