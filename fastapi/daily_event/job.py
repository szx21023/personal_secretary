async def job_daily_event_everyday_reminding():
    from customer.service import CustomerService
    from line.service import LineService
    from .service import DailyEventService

    print('job_daily_event_everyday_reminding start')

    # 取得今日所有的 daily_event
    daily_events = await DailyEventService.get_daily_event_today()

    customer_d = {}
    for daily_event in daily_events:
        customer_id = daily_event.customer_id
        if customer_id not in customer_d:
            customer_d[customer_id] = []

        customer_d[customer_id].append(daily_event)

    # 依據不同的 customer 各別通知
    for customer_id in customer_d:
        daily_events = customer_d[customer_id]
        customer = await CustomerService.get_customer_by_id(customer_id)
        line_uid = customer.line_uid

        for daily_event in customer_d[customer_id]:
            message = daily_event.event_name
            await LineService.push_message(line_uid, message)

    print('job_daily_event_everyday_reminding end')

async def job_daily_event_to_delayed():
    from customer.service import CustomerService
    from line.service import LineService
    from .service import DailyEventService

    print('job_daily_event_everyhour_delay start')

    # 取得今日所有的 daily_event
    daily_events = await DailyEventService.get_daily_event_waiting_but_delayed()

    customer_d = {}
    for daily_event in daily_events:
        customer_id = daily_event.customer_id
        if customer_id not in customer_d:
            customer_d[customer_id] = []

        customer_d[customer_id].append(daily_event)

    # 依據不同的 customer 各別通知
    for customer_id in customer_d:
        daily_events = customer_d[customer_id]
        customer = await CustomerService.get_customer_by_id(customer_id)
        line_uid = customer.line_uid

        for daily_event in customer_d[customer_id]:
            daily_event = await DailyEventService.to_delay(daily_event)
            message = daily_event.event_name
            await LineService.push_message(line_uid, message)

    print('job_daily_event_everyhour_delay end')