
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()

order_table = sqlalchemy.Table(
    'order',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("hash_inn", sqlalchemy.String),
    sqlalchemy.Column("okved2", sqlalchemy.Integer, default=-1),
    sqlalchemy.Column("need_search", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text('NOW()')),
    sqlalchemy.Column("date_load_pays", sqlalchemy.DateTime),    
    sqlalchemy.Column("date_start_search", sqlalchemy.DateTime),    
    sqlalchemy.Column("date_end_search", sqlalchemy.DateTime),    

)