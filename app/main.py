from fastapi import FastAPI, HTTPException
from typing import List
from datetime import date
import random

from .models import Quote, Order, PortfolioEntry, OrderResponse

app = FastAPI(title="Stock Trader API")

# In-memory stores
PORTFOLIO: List[PortfolioEntry] = []
ORDERS: List[Order] = []

@app.get("/", summary="Health check")
def read_root():
    return {"status": "ok"}

@app.get("/quote/{symbol}", response_model=Quote, summary="Get a fake stock quote")
def get_quote(symbol: str):
    # In a real app you'd fetch from an external API
    fake_price = round(random.uniform(10, 500), 2)
    return Quote(symbol=symbol.upper(), price=fake_price, timestamp=date.today())

@app.post("/orders/", response_model=OrderResponse, summary="Place a buy/sell order")
def place_order(order: Order):
    # simplistic fill logic: accept if price >= 0
    if order.price <= 0 or order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid price or quantity")
    ORDERS.append(order)
    # update portfolio for buys only
    if order.side == "buy":
        # find existing
        entry = next((e for e in PORTFOLIO if e.symbol == order.symbol), None)
        if entry:
            total_cost = entry.avg_price * entry.quantity + order.price * order.quantity
            entry.quantity += order.quantity
            entry.avg_price = total_cost / entry.quantity
        else:
            PORTFOLIO.append(PortfolioEntry(symbol=order.symbol,
                                            quantity=order.quantity,
                                            avg_price=order.price))
    return OrderResponse(order=order, status="accepted")

@app.get("/portfolio/", response_model=List[PortfolioEntry], summary="View portfolio")
def view_portfolio():
    return PORTFOLIO
