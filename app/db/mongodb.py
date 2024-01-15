import motor.motor_asyncio


class MongoDB:

    client: motor.motor_asyncio.AsyncIOMotorClient
    db: motor.motor_asyncio.AsyncIOMotorDatabase

    @staticmethod
    async def connect_to_db(connection_string: str):
        MongoDB.client = motor.motor_asyncio.AsyncIOMotorClient(
            connection_string)
        MongoDB.db = MongoDB.client['discord-clone']
        try:
            await MongoDB.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    @staticmethod
    async def close_db_connection():
        MongoDB.client.close()
        print("Closed connection to MongoDB")

    @staticmethod
    async def get_db():
        return MongoDB.db
