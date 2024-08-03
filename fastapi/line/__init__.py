from linebot import LineBotApi, WebhookHandler

def init_app(app):
    from .controller import router

    app.include_router(router)

    app.state.line_bot_api = LineBotApi(app.state.config.get('LINE_CHANNEL_ACCESS_TOKEN'))
    app.state.line_handler = WebhookHandler(app.state.config.get('LINE_CHANNEL_SECRET'))

    from linebot.models import MessageEvent, TextMessage
    @app.state.line_handler.add(MessageEvent, message=TextMessage)
    def handle_message(event: MessageEvent):
        app.state.line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=event.message.text)
        )
