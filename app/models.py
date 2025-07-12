from pydantic import BaseModel, Field
from typing import Literal, List
from datetime import date

class Quote(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol, e.g. AAPL")
    price: float = Field(..., ge=0, description="Current price per share")
    timestamp: date = Field(..., description="Date of the quote")

class Order(BaseModel):
    id: int
    symbol: str
    quantity: int = Field(..., gt=0)
    side: Literal['buy', 'sell']
    price: float = Field(..., ge=0)

class PortfolioEntry(BaseModel):
    symbol: str
    quantity: int
    avg_price: float

class OrderResponse(BaseModel):
    order: Order
    status: Literal['accepted', 'rejected']
