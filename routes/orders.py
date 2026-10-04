from datetime import datetime

from fastapi.params import Depends, Query
from sqlmodel import Session, select,func
from fastapi import APIRouter

from database import get_session
from models import Order,OrderUpdate,OrderCreated,status_log,status



router=APIRouter(prefix="/order",tags=["OrderStatus"])


@router.post("/",response_model=Order)
def order_add(order:OrderCreated,session:Session=Depends(get_session)):
    db_order=Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/",response_model=list[Order])
def list_orders(
        order_status:status = Query(None,description="Filter by order_status") ,
        created_at: str = Query(None, description="Filter by created date"),
        skip: int = Query(0,ge=0, description="How many records to be skipped"),
        limit : int =Query(10,ge=1,description="records displayed in one go"),
        session:Session=Depends(get_session)):
    query=select(Order)
    if order_status:
        query=query.where(Order.order_status==order_status)
    if created_at:
        # query=query.where(Order.created_at>=datetime.strptime(created_at,"%Y:%m:%d").min.time() and Order.created_at<=datetime.strptime(created_at,"%Y:%m:%d").max.time())
        query = query.where(Order.created_at.date() >= datetime.strptime(created_at,"%Y:%m:%d"))
    query=query.offset(skip).limit(limit)
    return session.exec(query).all()

