from datetime import datetime

from beanie import Document
from pydantic import Field

class InternalBaseDocument(Document):
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime = Field(default_factory=datetime.utcnow)

def return_response(data, page_no=1, page_size=20, code=200, message=None):
    if type(data) != list:
        data = [data] if data else []

    # 未來做 query 時，page_no, page_size 要重新修改
    page_size = len(data)
    ret = {}
    ret['data'] = {
        'page_data': data[(page_no-1)*page_size: page_no*page_size],
        'page_no': page_no,
        'page_size': page_size,
        'total_num': len(data)
    }
    ret['code'] = code
    ret['message'] = message

    return ret