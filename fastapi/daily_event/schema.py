# -*- coding: UTF-8 -*-
from marshmallow import fields, Schema

class DailyEventSchema(Schema):
    customer_id = fields.String()
    event_name = fields.String()
    event_type = fields.String()
    status = fields.String()

    description = fields.String()
    note = fields.String()
    estimated_start_time = fields.DateTime()
    estimated_end_time = fields.DateTime()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    cancel_time = fields.DateTime()

