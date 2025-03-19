from datetime import datetime
from fastapi import APIRouter, Body, Request

from utils import return_response

from .service import CustomerService

router = APIRouter(prefix=f"/customer", tags=["customer"])

@router.post("")
async def create_customer(schema = Body(example={
        'line_uid': 'U22280e5e05c960a92aac3a1a4a3e5d6a',
        'name': 'name'
    })):
    """
    post customer api
    """

    customer = await CustomerService.create_customer(**schema)
    return return_response(customer)