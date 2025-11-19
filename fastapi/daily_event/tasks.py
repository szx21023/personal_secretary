import requests
from celery import shared_task

from .const import DailyEventStatus

@shared_task(name="tasks.trigger_api")
def trigger_api_call(daily_event):
    from line.service import LineService

    if daily_event.status == DailyEventStatus.WAITING:
        LineService.remind_coming_daily_event(daily_event)