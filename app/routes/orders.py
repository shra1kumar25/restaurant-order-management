from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    table_id: int
    items: list[OrderItem]

class OrderStatus(str, Enum):
    PLACED = "PLACED"
    PREPARING = "PREPARING"
    READY = "READY"
    SERVED = "SERVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

orders = []


menu_items = [
    {
        "menu_item_id": 1,
        "item_name": "Chicken Biryani",
        "price": 250
    },
    {
        "menu_item_id": 2,
        "item_name": "Mutton Biryani",
        "price": 350
    },
    {
        "menu_item_id": 3,
        "item_name": "Veg Biryani",
        "price": 180
    },
    {
        "menu_item_id": 4,
        "item_name": "Coke",
        "price": 40
    }
]


@router.get("")
def get_orders():
    return orders


@router.get("/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate
):

    for order in orders:

        if order["order_id"] == order_id:

            order["status"] = status_update.status

            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )



@router.post("")
def create_order(order: OrderCreate):

    total_amount = 0

    for item in order.items:

        menu_item = next(
            (
                menu
                for menu in menu_items
                if menu["menu_item_id"] == item.menu_item_id
            ),
            None
        )

        if menu_item is None:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item.menu_item_id} not found"
            )

        total_amount += menu_item["price"] * item.quantity

    new_order = {
        "order_id": len(orders) + 101,
        "table_id": order.table_id,
        "items": order.items,
        "status": "PLACED",
        "total_amount": total_amount
    }

    orders.append(new_order)

    return new_order
@router.get("/{order_id}/bill")
def get_order_bill(order_id: int):

    for order in orders:

        if order["order_id"] == order_id:

            subtotal = order["total_amount"]
            gst = subtotal * 0.05
            grand_total = subtotal + gst

            return {
                "order_id": order["order_id"],
                "table_id": order["table_id"],
                "subtotal": subtotal,
                "gst": gst,
                "grand_total": grand_total
            }

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )
@router.delete("/{order_id}")
def delete_order(order_id: int):

    for index, order in enumerate(orders):

        if order["order_id"] == order_id:

            deleted_order = orders.pop(index)

            return {
                "message": "Order deleted successfully",
                "order": deleted_order
            }

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )
