# db.py
import motor.motor_asyncio
from config import MONGO_DB_URI

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name, username=None):
        return dict(
            id=id,
            name=name,
            username=username or "N/A"  # store N/A if username not set
        )
    
    async def add_user(self, id, name, username=None):
        user = self.new_user(id, name, username)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

db = Database(MONGO_DB_URI, "SessionsNeon")

# Dont remove Credits
# Developer Telegram @MyselfNeon
# Update channel - @NeonFiles
