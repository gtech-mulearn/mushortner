from decouple import config
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from urllib.parse import quote_plus

class DBConnection:
    def __init__(self, pool_size=5, max_overflow=10):
        db_host = config("db_host")
        db_user = config("db_user")
        db_pass = quote_plus(config("db_pass"))
        db_name = config("db_name")
        self.db_engine = create_engine(
            url=f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}',
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )

    def execute(self, query, params=None):
        with Session(self.db_engine) as session:
            session.execute(text(query), params)
            session.commit()

    def fetch_all(self, query, params=None):
        with Session(self.db_engine) as session:
            result = session.execute(text(query), params)
            session.commit()
            return result.fetchall()

    def fetch_one(self, query, params=None):
        with Session(self.db_engine) as session:
            result = session.execute(text(query), params)
            session.commit()
            return result.fetchone()

    def fetch_single_data(self, query, params=None):
        result = self.fetch_one(query, params)
        if result and result[0]:
            return result[0]
