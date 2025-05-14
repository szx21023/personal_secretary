from fastapi_basic.ext.line import LineBot

class LineBot(LineBot):
    def __init__(self, channel_access_token: str, channel_secret: str, logger=None):
        super().__init__(channel_access_token, channel_secret, logger)

    async def handle_message(self, event):
        from .service import LineService
        await LineService.handle_message(event)

def init_app(app):
    from .controller import router

    app.include_router(router)

    line_bot = LineBot(app.state.config.get('LINE_CHANNEL_ACCESS_TOKEN'), app.state.config.get('LINE_CHANNEL_SECRET'), app.logger)
    app.state.line_bot = line_bot
