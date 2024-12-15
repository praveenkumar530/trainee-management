from app.queries.gym_queries import GymQuery
from app.models.gym import UserDataRequest

class GymService:
    def __init__(self, query: GymQuery):
        self.query = query

    async def fetch_all_members(self):
        data = await self.query.get_all_users()
        print(data)
        return  data

    async def add_user(self, input_data: UserDataRequest):
        try:
            data = await self.query.add_user(input_data)
            print(data)
            return {"message":" success"}
        except Exception as e:
            print(e)
            return  {"message": "failure"}

    async def delete_user(self, user_id: int):
        try:
            data = await self.query.delete_user(user_id)
            print(data)
            return {"message":" success"}
        except Exception as e:
            print(e)
            return  {"message": "failure"}

    async def get_users_by_trainer_id(self, trainer_email: str):
        try:
            data = await self.query.get_users_by_trainer_id(trainer_email)
            return data
        except Exception as e:
            print(e)
            return  {"message": "failure"}