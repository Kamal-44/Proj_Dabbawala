from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime, timezone
import pytz

# ist_tz=pytz.timezone("Asia/kolkata")
ist_tz=pytz.timezone("Asia/Kolkata")


class status(str,Enum):
    PREPARING="preparing"
    PICKEDUP="picked up"
    INTRANSIT="in transit"
    DELIVERED="delivered"


class Order(SQLModel,table=True):
    order_id:Optional[int]=Field(default=None,primary_key=True)
    customer_name:str
    customer_address:str
    item:str
    order_status:status=Field(default=status.PREPARING)
    created_at:datetime=Field(default_factory=lambda :datetime.now(timezone.utc))

class OrderCreated(SQLModel):
    customer_name:str
    customer_address:str
    item:str

class OrderUpdate(SQLModel):
    customer_address:Optional[str]=Field(None)
    order_status:status

class status_log(SQLModel):
    order_id:int
    old_status:status
    new_status:status
    updated_at:datetime