from linebot.models import MessageEvent, TextMessage

from main import app
from daily_event.service import DailyEventService
from daily_event.schema import DailyEventSchema

from .template import GetDailyTemplate

class LineService:
    @staticmethod
    async def handle_message(event):
        if '建立' in event.message.text:
            result = await LineService.create_daily_event(event)

        elif '查看' in event.message.text:
            result = await LineService.get_daily_event(event)

        else:
            app.state.line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text=event.message.text)
            )

    @staticmethod
    async def create_daily_event(event):
        text = event.message.text.replace('建立', '')
        event_name, event_type = text.split(' ')
        daily_event = await DailyEventService.create_daily_event(event_name, event_type)
        return daily_event

    @staticmethod
    async def get_daily_event(event):
        daily_events = await DailyEventService.get_daily_event()
        schema = DailyEventSchema(many=True)
        daily_events = schema.dump(daily_events)

        message_list = []
        for daily_event in daily_events:
            template = GetDailyTemplate(**daily_event)
            message_list.append(template.message)

        app.state.line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='\n'.join(message_list))
        )
        return daily_events