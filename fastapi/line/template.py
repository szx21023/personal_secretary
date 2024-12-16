class BaseTemplate:
    def __init__(self, event_name=None, event_type=None, status=None, description=None, note=None, estimated_start_time=None, \
            estimated_end_time=None, start_time=None, end_time=None, cancel_time=None, **kwargs):

        self.event_name = event_name
        self.event_type = event_type
        self.status = status

        self.description = description
        self.note = note
        self.estimated_start_time = estimated_start_time
        self.estimated_end_time = estimated_end_time
        self.start_time = start_time
        self.end_time = end_time
        self.cancel_time = cancel_time

        self.message = ''

class GetDailyTemplate(BaseTemplate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.message = f'{self.event_name}, {self.event_type}, {self.status}, {self.estimated_start_time}, {self.estimated_end_time}'
