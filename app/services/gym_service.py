from app.queries.gym_queries import GymQuery
from app.models.gym import UserDataRequest, ExerciseDataRequest, SuperSetDataRequest

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


    async def get_exercise_types(self,):
        try:
            db_data = await self.query.get_exercise_types()
            data = [{"id": i["id"], "exercise_name":i["name"]} for i in db_data]
            return data
        except Exception as e:
            print(e)
            return  {"message": "failure"}

    async def add_exercise_type(self, input_data: ExerciseDataRequest):
        try:
            # TODO : add existing types check before adding new one
            data = await self.query.add_exercise_type(input_data)
            return {"message":" success"}
        except Exception as e:
            print(e)
            return  {"message": "failure"}

    async def delete_exercise_type(self, type_id: int):
        try:
            data = await self.query.delete_exercise_type(type_id)
            print(data)
            return {"message":" success"}
        except Exception as e:
            print(e)
            return  {"message": "failure"}


    async def add_super_set(self, input_data: SuperSetDataRequest):
        try:
            return await self.query.insert_superset_and_exercises(input_data)
        except Exception as e:
            print(e)
            return  {"message": "failure"}
