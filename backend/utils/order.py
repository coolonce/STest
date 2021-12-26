from datetime import datetime

from sqlalchemy import schema, desc, func, select
from connects import database

from models.order import order_table

from shemas.order import Order_Create, OrderModel

async def create_order(order: Order_Create):
    return 1
    query = (
        order_table.insert()
        .values(
            created_at=datetime.now(),
        )
        .returning(
            order_table.c.id,
            order_table.c.created_at,
        )
    )
    order = await database.fetch_one(query)

    order = dict(zip(order, order.values()))

    return order

async def get_order(order_id: int):
    query = (
        select(
            [
                order_table.c.id,
                order_table.c.need_search
            ]
        )
        .where(order_table.c.id == order_id)
    )
    return await database.fetch_one(query)

async def update_order(order_id: int, title, values):
    query = (
        order_table.update()
        .where(order_table.c.id == order_id)
        .values(title=title, content=values)
    )
    return await database.execute(query)