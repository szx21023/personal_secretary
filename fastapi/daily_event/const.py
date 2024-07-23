class DailyEventStatus:
    '''
    閒置中：尚無預計執行時間
    未開始：未到預計開始時間
    已開始：存在實際開始時間
    已逾時：超過預計結束時間
    已完成：存在實際結束時間
    '''
    IDLE = "idle"
    WAITING = "waiting"
    STARTED = "started"
    OVERTIME = "overtime"
    FINISHED = "finished"
