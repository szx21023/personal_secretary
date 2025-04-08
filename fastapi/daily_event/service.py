from datetime import timedelta

from main import app
from exception.exception import EstimatedTimeWrongValueException, EventNameNotExistException, EventTypeIllegalException, EventStatusNotWaitingException, EventAlreadyExistAtSameTimeException

from .const import DailyEventStatus, DailyEventType
from .model import DailyEvent
from .schema import DailyEventSchema

from customer.service import CustomerService
from utils import system_tz, get_local_now_time, get_local_today_time_to_utc

class DailyEventService:
    @staticmethod
    async def create_daily_event(customer_id, event_name, event_type, **kargs):
        customer = await CustomerService.get_customer_by_id(customer_id)

        schema = DailyEventSchema()
        data = schema.load(kargs)
        # if nether (both columns exist) nor (both columns not exist), raise error
        estimated_start_time = data.get('estimated_start_time')
        estimated_end_time = data.get('estimated_end_time')
        if not ((estimated_start_time and estimated_end_time) or \
        (not estimated_start_time and not estimated_end_time)):
            exception = EstimatedTimeWrongValueException()
            app.logger.warning(exception.message)
            raise exception

        if estimated_end_time and estimated_start_time:
            if estimated_end_time < estimated_start_time:
                exception = EstimatedTimeWrongValueException()
                app.logger.warning(exception.message)
                raise exception

            if daily_event := await DailyEventService.check_time_overlap(estimated_start_time, estimated_end_time):
                exception = EventAlreadyExistAtSameTimeException()
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

        if 'start_time' in data:
            data['status'] = DailyEventStatus.STARTED

        elif 'estimated_start_time' in data:
            data['status'] = DailyEventStatus.WAITING

        else:
            data['status'] = DailyEventStatus.IDLE

        data.update({
            'customer_id': customer_id,
            'event_name': event_name,
            'event_type': event_type
        })
        daily_event = DailyEvent(**data)
        await daily_event.save()

        await DailyEventService.setup_schedule_remind(daily_event)
        daily_event = schema.dump(daily_event)
        return daily_event

    @staticmethod
    async def get_daily_event():
        daily_events = await DailyEvent.find().sort("-create_time").to_list()
        return daily_events

    @staticmethod
    async def get_daily_event_today():
        today = get_local_today_time_to_utc()
        daily_events = await DailyEvent.find({
            "estimated_start_time": {"$gte": today, "$lt": today + timedelta(days=1)}
        }).sort("estimated_start_time").to_list()
        return daily_events

    @staticmethod
    async def get_daily_event_waiting_but_delayed():
        current_time = get_local_now_time()
        daily_events = await DailyEvent.find({
            "status": DailyEventStatus.WAITING,
            "estimated_start_time": {"$lt": current_time}
        }).sort("estimated_start_time").to_list()
        return daily_events

    @staticmethod
    async def to_delay(daily_event):
        if daily_event.status != DailyEventStatus.WAITING:
            exception = EventStatusNotWaitingException(daily_event=daily_event)
            app.logger.warning(exception.message)
            raise exception

        daily_event.status = DailyEventStatus.DELAYED
        await daily_event.save()
        message = f'daily_event changed to delayed, daily_event: {str(daily_event.id)}'
        app.logger.warning(message)
        return daily_event

    @staticmethod
    async def setup_schedule_remind(daily_event):
        from line.service import LineService

        if daily_event.status == DailyEventStatus.WAITING:
            job_id = f'job_remind_coming_daily_event_{str(daily_event.id)}'
            run_date = daily_event.estimated_start_time.replace(tzinfo=system_tz())
            job = app.scheduler.add_job(LineService.remind_coming_daily_event, 'date', run_date=run_date, id=job_id, args=[daily_event])
            message = f"setup job_remind_coming_daily_event, job_id: {job_id}, run_date: {run_date}"
            app.logger.info(message)

    @staticmethod
    async def check_time_overlap(start_time, end_time):
        # 查詢是否存在時間有交集的資料
        daily_event = await DailyEvent.find({
            "estimated_start_time": {"$lt": end_time},
            "estimated_end_time": {"$gt": start_time}
        }).first_or_none()
        return daily_event