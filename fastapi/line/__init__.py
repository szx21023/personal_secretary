import asyncio

from fastapi_basic.ext.line import LineBot

from linebot.models import MessageEvent, TextMessage

def init_app(app):
    from .controller import router
    from .service import LineService

    app.include_router(router)

    line_bot = LineBot(app.state.config.get('LINE_CHANNEL_ACCESS_TOKEN'), app.state.config.get('LINE_CHANNEL_SECRET'))
    app.state.line_bot = line_bot

    @app.state.line_bot.handler.add(MessageEvent, message=TextMessage)
    def handle_message(event: MessageEvent):
        message = f'line_event: {event}'
        app.logger.info(message)
        asyncio.create_task(LineService.handle_message(event))
