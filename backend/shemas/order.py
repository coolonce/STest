from pydantic import BaseModel

class Order_Create(BaseModel):
    pass


class OrderModel(BaseModel):
    id: int
    need_search: bool
    