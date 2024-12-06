from typing import Optional

from pydantic import Field

from utils import InternalBaseDocument

class Customer(InternalBaseDocument):
    line_uid: str

    name: Optional[str] = Field(None)

    class Settings:
        name = "customer"