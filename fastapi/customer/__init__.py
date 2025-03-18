async def init_app(app):
    from .model import Customer
    data = {'line_uid': 'U22280e5e05c960a92aac3a1a4a3e5d6a'}
    customer = Customer(**data)
    await customer.save()
