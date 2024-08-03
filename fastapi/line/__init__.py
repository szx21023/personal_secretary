from linebot import LineBotApi, WebhookHandler

def init_app(app):
    from .controller import router

    app.include_router(router)

    app.state.line_bot_api = LineBotApi(app.state.config.get('LINE_CHANNEL_ACCESS_TOKEN'))
    app.state.line_handler = WebhookHandler(app.state.config.get('LINE_CHANNEL_SECRET'))
