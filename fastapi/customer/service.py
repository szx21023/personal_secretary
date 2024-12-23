from bson import ObjectId

from .model import Customer
from exception.exception import CustomerNotExistException
from main import app

class CustomerService:
    async def get_by_id(customer_id):
        if not (customer := await Customer.find({"_id": ObjectId(customer_id)}).first_or_none()):
            message = f'no customer, customer_id: {customer_id}'
            app.logger.info(message)
            return

        return customer

    async def get_by_line_uid(line_uid):
        if not (customer := await Customer.find({"line_uid": line_uid}).first_or_none()):
            message = f'no customer, line_uid: {line_uid}'
            app.logger.info(message)
            return

        return customer
    
    @staticmethod
    async def get_customer_by_id(customer_id):
        if not (customer := await CustomerService.get_by_id(customer_id)):
            exception = CustomerNotExistException()
            app.logger.warning(exception.message)
            raise exception

        return customer

    async def create_customer(schema):
        customer = Customer(**schema)
        await customer.save()
        return customer