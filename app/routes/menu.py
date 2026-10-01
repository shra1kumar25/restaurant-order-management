from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu"]
)


class MenuItemCreate(BaseModel):
    item_name: str
    price: float


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
def get_menu_items():
    return menu_items


@router.post("")
def create_menu_item(item: MenuItemCreate):

    new_item = {
        "menu_item_id": len(menu_items) + 1,
        "item_name": item.item_name,
        "price": item.price
    }

    menu_items.append(new_item)

    return new_item


@router.get("/{menu_item_id}")
def get_menu_item(menu_item_id: int):

    for item in menu_items:

        if item["menu_item_id"] == menu_item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )


@router.put("/{menu_item_id}")
def update_menu_item(
    menu_item_id: int,
    item_data: MenuItemCreate
):

    for item in menu_items:

        if item["menu_item_id"] == menu_item_id:

            item["item_name"] = item_data.item_name
            item["price"] = item_data.price

            return item

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )
@router.delete("/{menu_item_id}")
def delete_menu_item(menu_item_id: int):

    for index, item in enumerate(menu_items):

        if item["menu_item_id"] == menu_item_id:

            deleted_item = menu_items.pop(index)

            return {
                "message": "Menu item deleted successfully",
                "item": deleted_item
            }

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )
