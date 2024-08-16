import asyncpg
from contextlib import asynccontextmanager

# App modules:
import constants


async def postgres_async(database, server):
    conn = await asyncpg.connect(
        database=database,
        user=constants.not_the_best_idea['a'],
        host=constants.not_the_best_idea[server],
        password=constants.not_the_best_idea['b']
    )
    return conn


class AsyncContextDB:
    def __init__(self, server, database_name, provide_conn=False):
        self.database_name = database_name
        self.provide_conn = provide_conn
        self.server = server
        self.conn = None
        self.transaction = None

    async def __aenter__(self):
        self.conn = await postgres_async(self.database_name, self.server)
        self.transaction = self.conn.transaction()
        await self.transaction.start()
        if self.provide_conn:
            return self.conn
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self.transaction.commit()
            else:
                await self.transaction.rollback()
        except Exception as e:
            await self.transaction.rollback()
            raise Exception('>>> Via AsyncContextDB: ' + str(e))
        finally:
            await self.conn.close()

    @asynccontextmanager
    async def nested_transaction(self):
        async with self.conn.transaction():
            yield self.conn
