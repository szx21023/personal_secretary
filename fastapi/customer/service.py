from bson import ObjectId

from .model import Customer
from exception.exception import CustomerNotExistException, CustomerCreatedFailException
from main import app

class CustomerService:
    @staticmethod
    async def get_by_id(customer_id):
        if not (customer := await Customer.find({"_id": ObjectId(customer_id)}).first_or_none()):
            message = f'no customer, customer_id: {customer_id}'
            app.logger.info(message)
            return

        return customer

    @staticmethod
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

    @staticmethod
    async def create_customer(**kwargs):
        try:
            customer = Customer(**kwargs)
            await customer.save()
            message = f'Create customer successfully, data: {kwargs}'
            app.logger.info(message)

        except Exception as e:
            exception = CustomerCreatedFailException()
            app.logger.warning(exception.message)
            raise exception

        return customer

    @staticmethod
    async def get_customer():
        customers = await Customer.find().sort("-create_time").to_list()
        return customers