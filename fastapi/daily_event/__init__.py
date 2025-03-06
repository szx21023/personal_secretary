from apscheduler.triggers.cron import CronTrigger

def init_app(app):
    from .controller import router
    from .job import job_daily_event_everyday_reminding, job_daily_event_to_delayed

    app.include_router(router)

    job_configs = [
        ('CRON_DAILY_EVENT_EVERYDAY_REMINDING', job_daily_event_everyday_reminding),
        ('CRON_DAILY_EVENT_DELAY', job_daily_event_to_delayed)
    ]
    for job_config in job_configs:
        config_key = job_config[0]
        job_func = job_config[1]
        app.scheduler.add_job(
            job_func,
            trigger=CronTrigger.from_crontab(app.state.config[config_key]),
            max_instances=1,
            replace_existing=True,
            misfire_grace_time=None
        )