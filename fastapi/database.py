from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import Settings
from customer.model import Customer
from daily_event.model import DailyEvent

async def init_db():
    db_settings = Settings().dict().get("MONGODB_SETTINGS")
    username = db_settings.get("username")
    password = db_settings.get("password")
    host = db_settings.get("host")
    port = db_settings.get("port")
    db_name = db_settings.get("db_name")
    ssl = db_settings.get("ssl")
    ssl_ca_certs = db_settings.get("ssl_ca_certs")

    db_settings = dict(
        username=username,
        password=password,
        host=host,
        port=port,
        retryWrites=False
    )
    if ssl:
        db_settings["ssl"] = ssl

    if ssl_ca_certs and ssl_ca_certs != "":
        db_settings["tlsCAFile"] = ssl_ca_certs

    client = AsyncIOMotorClient(**db_settings)
    await init_beanie(database=client[db_name], document_models=[Customer, DailyEvent])
