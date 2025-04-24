from fastapi_basic.database.mongodb import MongoDB

from customer.model import Customer
from daily_event.model import DailyEvent

async def init_db(app):
    settings = app.state.config.get("MONGODB_SETTINGS")
    db = MongoDB(
        username=settings.get("username"),
        password=settings.get("password"),
        host=settings.get("host"),
        port=settings.get("port"),
        db_name=settings.get("db_name"),
        ssl=settings.get("ssl"),
        ssl_ca_certs=settings.get("ssl_ca_certs")
    )
    await db.connect(document_models=[Customer, DailyEvent])