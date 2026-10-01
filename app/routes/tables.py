from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)


class TableCreate(BaseModel):
    table_number: str
    capacity: int


tables = [
    {
        "table_id": 1,
        "table_number": "T01",
        "capacity": 4
    }
]


@router.get("")
def get_tables():
    return tables


@router.post("")
def create_table(table: TableCreate):

    new_table = {
        "table_id": len(tables) + 1,
        "table_number": table.table_number,
        "capacity": table.capacity
    }

    tables.append(new_table)

    return new_table


@router.get("/{table_id}")
def get_table(table_id: int):

    for table in tables:

        if table["table_id"] == table_id:
            return table

    raise HTTPException(
        status_code=404,
        detail="Table not found"
    )


@router.put("/{table_id}")
def update_table(table_id: int, table_data: TableCreate):

    for table in tables:

        if table["table_id"] == table_id:

            table["table_number"] = table_data.table_number
            table["capacity"] = table_data.capacity

            return table

    raise HTTPException(
        status_code=404,
        detail="Table not found"
    )
@router.delete("/{table_id}")
def delete_table(table_id: int):

    for index, table in enumerate(tables):

        if table["table_id"] == table_id:

            deleted_table = tables.pop(index)

            return {
                "message": "Table deleted successfully",
                "table": deleted_table
            }

    raise HTTPException(
        status_code=404,
        detail="Table not found"
    )
