from datetime import datetime
from fastapi import APIRouter, Body, Request

from utils import return_response

from .service import DailyEventService

router = APIRouter(prefix=f"/daily_event", tags=["daily_event"])

@router.post("")
async def create_daily_event(schema = Body(example={
        'event_name': 'event_name',
        'event_type': 'event_type',
        'estimated_start_time': '2024-07-22 15:30:00',
        'estimated_end_time': '2024-07-23 00:00:00'
    })):
    """
    post daily_event api
    """

    event_name = schema.get('event_name')
    event_type = schema.get('event_type')
    estimated_start_time = schema.get('estimated_start_time')
    estimated_end_time = schema.get('estimated_end_time')

    daily_events = await DailyEventService.create_daily_event(event_name, event_type, estimated_start_time, estimated_end_time)
    return return_response(daily_events)

@router.get("")
async def get_daily_event():
    """
    get daily_event api
    """

    daily_events = await DailyEventService.get_daily_event()
    return return_response(daily_events)