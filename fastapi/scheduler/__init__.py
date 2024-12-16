from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient

from .const import MISFIRE_GRACE_TIME

async def init_app(app):
    # 连接 MongoDB
    db_user = app.state.config.get('MONGODB_SETTINGS').get('username')
    db_pass = app.state.config.get('MONGODB_SETTINGS').get('password')
    db_host = app.state.config.get('MONGODB_SETTINGS').get('host')
    db_port = app.state.config.get('MONGODB_SETTINGS').get('port')
    db_name = app.state.config.get('MONGODB_SETTINGS').get('db_name')
    db_cert = app.state.config.get('MONGODB_SETTINGS').get('ssl_ca_certs')

    if app.state.config.get('MONGODB_SETTINGS').get('ssl'):
        url = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?retryWrites=false&authSource={db_name}"
        client = MongoClient(url, tls=True, tlsAllowInvalidHostnames=True, tlsCAFile=db_cert)

    elif db_user and db_pass:
        url = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}"
        client = MongoClient(url)

    else:
        url = f"mongodb://{db_host}:{db_port}"
        client = MongoClient(url)

    # 创建一个 job store 实例
    job_store = MongoDBJobStore(database=db_name, collection='jobs', client=client)

    # 创建一个调度器
    scheduler = AsyncIOScheduler(job_defaults={'misfire_grace_time': MISFIRE_GRACE_TIME})
    scheduler.add_jobstore(job_store)

    # 启动调度器
    app.scheduler = scheduler
    app.scheduler.start()