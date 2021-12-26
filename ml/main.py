from datetime import datetime
import pandas as pd
import numpy as np
import pickle


from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.neighbors import KNeighborsClassifier

# from sklearn.preprocessing import Normalizer

import os
import redis

import sqlalchemy
from sqlalchemy import create_engine

from const import (
    CODE_DIR_NOT_FOUND, 
    CODE_FILE_NOT_FOUND,
    DB_TABLE, 
    LOCAL_STORAGE,
    MODEL_PATH,
    REDIS_HOST,
    REDIS_QUEUE,
    REDIS_STATUS_ORDER,
    SQLALCHEMY_DATABASE_URL
    )



rds = redis.StrictRedis(host=REDIS_HOST)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

model = pickle.load(open(MODEL_PATH, 'rb'))

def update_data_in_db(order_id: int, column: str, value):
    return engine.connect().execute(f"update {DB_TABLE} set {column} = {value} where order_id = {order_id}")

def get_data(order_id: int):
    dirpath = f"{LOCAL_STORAGE}/{order_id}"
    if not os.path.exists(dirpath):
        return CODE_DIR_NOT_FOUND

    filepath = f"{dirpath}/data.csv"
    if not os.path.isfile(filepath):
        return CODE_FILE_NOT_FOUND

    return pd.read_csv(filepath=filepath)


def prepared_data(order_id: int):
    pays_df = get_data(order_id)
    if isinstance(pays_df, int):
        return pays_df
    
    pays_df = pays_df.groupby(['hash_inn_kt', 'week']).agg({'sum': np.mean, 'count': np.mean})
    pays_df = pays_df.reset_index()
    
    features = ['week', 'count', 'sum']
    return pays_df[features]

    # scaler = Normalizer()
    # X = scaler.fit_transform(X)

    # pass

def classify_process():
    while True:
        with rds.pipeline() as pipe:
            pipe.rpop(REDIS_QUEUE)
            order_id, _ = pipe.execute()
        X = prepared_data(order_id)
        update_data_in_db(order_id, 'date_start_search', datetime.now)
        y = model.predict(X)
        update_data_in_db(order_id, 'date_end_search', datetime.now)
        if y >= 0:
            update_data_in_db(order_id, 'okved2', y)
        else:
            update_data_in_db(order_id, 'status', y)        
        rds.set(f"{REDIS_STATUS_ORDER}-{order_id}", y)

if __name__ == "__main__":    
    classify_process()