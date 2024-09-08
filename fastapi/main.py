import watchtower

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import logging
import traceback

from aws import init_app as init_aws_app
from daily_event import init_app as init_daily_event_app
from line import init_app as init_line_app
from config import Settings
from database import init_db
from version import version

class PSFactory:
    logger_name = 'my_log'
    log_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')

    def __setup_main_logger(self, app, logger_name=logger_name, level=logging.DEBUG):
        logger = self.__setup_logger(app, logger_name, level)
        app.logger = logger

    def __setup_logger(self, app, logger_name, level=logging.INFO):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.log_formatter)
        logger.addHandler(stream_handler)
        return logger

    def __setup_cloud_log(self, app):
        if app.state.aws_session and app.state.config.get("AWS_LOGGROUP_NAME"):
            logs_client = app.state.aws_session.client("logs")
            watchtower_handler = watchtower.CloudWatchLogHandler(
                log_group_name=app.state.config.get("AWS_LOGGROUP_NAME"),
                boto3_client=logs_client, create_log_group=True)
            watchtower_handler.setFormatter(self.log_formatter)
            app.logger.addHandler(watchtower_handler)

    def create_app(self):
        settings = Settings().dict()
        app = FastAPI(docs_url=settings.get('DOCS_URL'), redoc_url=settings.get('REDOC_URL'), openapi_url=settings.get('OPENAPI_URL'))
        app.state.config = settings
        app.state.aws_session = init_aws_app(app)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.__setup_main_logger(app, self.logger_name)
        self.__setup_logger(app, self.logger_name)
        self.__setup_cloud_log(app)

        @app.exception_handler(HTTPException)
        async def custom_http_exception_handler(request, exc):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "code": exc.detail["code"],
                    "message": exc.detail["message"],
                    "data": exc.detail["data"]
                }
            )

        @app.middleware("http")
        async def handle_request_headers(request: Request, call_next):
            app.logger.info(f"request.headers: {request.headers}")
            response = await call_next(request)
            return response

        return app

app = PSFactory().create_app()

@app.on_event("startup")
async def start_db():
    await init_db()
    init_daily_event_app(app)
    init_line_app(app)

@app.get("/hello")
def read_root():
    return {
        'data': {
            'version': version
        }
    }
