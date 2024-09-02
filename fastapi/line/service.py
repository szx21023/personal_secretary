from linebot.models import MessageEvent, TextMessage

from main import app

class LineService:
    @staticmethod
    async def handle_message(event):
        app.state.line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=event.message.text)
        )