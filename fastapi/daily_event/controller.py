from fastapi import APIRouter, Body

from utils import return_response

from .service import DailyEventService

router = APIRouter(prefix=f"/daily_event", tags=["daily_event"])

@router.post("")
async def create_daily_event(schema = Body(example={
        'customer_id': '',
        'event_name': 'event_name',
        'event_type': 'event_type',
        'estimated_start_time': '2024-07-22 15:30:00',
        'estimated_end_time': '2024-07-23 00:00:00'
    })):
    """
    post daily_event api
    """

    customer_id = schema.pop('customer_id')
    event_name = schema.pop('event_name')
    event_type = schema.pop('event_type')

    daily_events = await DailyEventService.create_daily_event(customer_id, event_name, event_type, **schema)
    return return_response(daily_events)

@router.get("")
async def get_daily_event():
    """
    get daily_event api
    """

    daily_events = await DailyEventService.get_daily_event()
    return return_response(daily_events)