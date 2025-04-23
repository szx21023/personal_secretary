from fastapi_basic.base_factory import BaseFactory

from customer import init_app as init_customer_app
from daily_event import init_app as init_daily_event_app
from line import init_app as init_line_app
from frontend_fastapi import init_app as init_frontend_fastapi_app
from scheduler import init_app as init_scheduler_app
from config import Settings
from database import init_db
from version import version

class PSFactory(BaseFactory):
    def get_app_config(self):
        config = Settings().dict()
        return config

    def create_the_app(self):
        app = self.create_app()

        return app

app = PSFactory().create_the_app()

@app.on_event("startup")
async def start_db():
    await init_db()
    await init_scheduler_app(app)
    await init_customer_app(app)
    init_daily_event_app(app)
    init_line_app(app)
    init_frontend_fastapi_app(app)

@app.get("/hello")
def read_root():
    return {
        'data': {
            'version': version
        }
    }
