from datetime import datetime,date
from fastapi.params import Depends, Query
from sqlmodel import Session, select,func
from fastapi import APIRouter
from database import get_session
from models import Order,OrderUpdate,OrderCreated,status_log,status

router=APIRouter(prefix="/stats",tags=["Status of orders"])


@router.get("/")
def daily_stats(
        summary_date:date | None=Query(None,description="filter by date given"),
        session : Session=Depends(get_session) ):
    total=0
    summary={}
    if not summary_date:
        summary_date=date.today()
    min_date = datetime.combine(summary_date, datetime.min.time())
    max_date = datetime.combine(summary_date, datetime.max.time())
    for order_status in status:
       result=session.exec(select(func.count(Order.order_id)).where(Order.created_at >= min_date, Order.created_at <= max_date, Order.order_status==order_status)).one()
       summary[order_status]=result
       total+=result

    return {
        "date":summary_date.isoformat(),
        "total_orders":total,
        "by status":summary
    }







