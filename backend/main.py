from datetime import datetime
import databases
from fastapi import (
    FastAPI, 
    File, 
    UploadFile,
    status
)
from fastapi.responses import JSONResponse
from connects import LOCAL_STORAGE, REDIS_QUEUE, redis, database
from shemas.order import OrderModel
from utils import order as order_utils

import os
import aiofiles


app = FastAPI(debug = True)


# @app.on_event("startup")
# async def startup():
#     # когда приложение запускается устанавливаем соединение с БД
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     # когда приложение останавливается разрываем соединение с БД
#     await database.disconnect()

@app.post("/order/create")
async def create_order():
    try:
        order = OrderModel()
        order =  await order_utils.create_order(order)
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
        )
    else:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'code': 'ok', 'order_id': order.id}
        )


##TODO 
# Добавить проверку на расширение
# Добавить определение разделителя в csv
@app.post("/order/{order_id}/upload-pays")
async def save_pays(order_id: int, file: UploadFile = File(...)):
    try:
        if not os.path.exists(os.path.join(os.getcwd(), LOCAL_STORAGE, str(order_id))):
            os.mkdir(f"{LOCAL_STORAGE}/{order_id}")
        async with aiofiles.open(f"{LOCAL_STORAGE}/{order_id}/data.csv", 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write

    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
        )
    else:
        order_utils.update_order(order_id, 'date_load_pays', datetime.now)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'code': 'ok', 'order_id': order_id}
        )

@app.post('/order/{order_id}/find')
async def start_find(order_id:int):
    try:
        order_utils.update_order(order_id, 'need_search', False)
        redis.rpush(REDIS_QUEUE, order_id)
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
        )
    else:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'code': 'ok', 'order_id': order_id}
        )