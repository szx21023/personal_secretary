import asyncio

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage

def init_app(app):
    from .controller import router
    from .service import LineService

    app.include_router(router)

    app.state.line_bot_api = LineBotApi(app.state.config.get('LINE_CHANNEL_ACCESS_TOKEN'))
    app.state.line_handler = WebhookHandler(app.state.config.get('LINE_CHANNEL_SECRET'))

    @app.state.line_handler.add(MessageEvent, message=TextMessage)
    def handle_message(event: MessageEvent):
        asyncio.create_task(LineService.handle_message(event))
