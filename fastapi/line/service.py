import asyncio
from linebot.models import MessageEvent, TextMessage

from main import app

class LineService:
    @staticmethod
    def handle_message(event):
        result = asyncio.create_task(LineService.async_function())
        return result
        # app.state.line_bot_api.reply_message(
        #     event.reply_token,
        #     TextMessage(text=event.message.text)
        # )


    async def async_function():
        print(123)
        await asyncio.sleep(1)
        return "Hello, World!"