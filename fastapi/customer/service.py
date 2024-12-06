from .model import Customer
from main import app

class CustomerService:
    async def get_by_line_uid(line_uid):
        if not (customer := await Customer.find({"line_uid": line_uid}).first_or_none()):
            message = f'no customer, line_uid: {line_uid}'
            app.logger.info(message)
            return

        return customer
    
    async def create_customer(schema):
        customer = Customer(**schema)
        await customer.save()
        return customer