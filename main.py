from fastapi import FastAPI, APIRouter, HTTPException, Query
from contextlib import asynccontextmanager
from routes.orders import router as order_router
from routes.stats import router as stats_router
from database import create_table


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_table()
    print("database table  created")
    yield
    # shutdown : cleanup
    print("Shutting down the app")


app=FastAPI(
    title="Dabbawala order system for correct update",
    description="different orders their id and their status in real time",
    lifespan = lifespan
)

app.include_router(order_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return{
        "message":"welcome to Dabbawalla service center"
    }