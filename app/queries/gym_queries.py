from typing import List
from core.database.database_conn import fetch_all, insert, update, connection_pool
from app.models.gym import UserDataRequest, ExerciseDataRequest, SuperSetDataRequest
from datetime import datetime
from core.logging_config import logger

class GymQuery:

    def __init__(self):
        self.users = "public.users"
        self.mapping = "public.trainer_user_mapping"
        self.exercise_types = "public.exercise_types"
        self.super_sets = "public.super_sets"
        self.exercise  = "public.exercise"


    async def get_all_users(self) -> List[dict]:
        get_query = f'''SELECT u.id, concat(u.first_name, ' ', u.last_name) as Name,  u.email, u.phone, m.trainer_id ,
	                    concat(t.first_name, ' ', t.last_name) as trainer_name  FROM  {self.users} u 
                        LEFT JOIN {self.mapping} m on m.user_id= u.id 
                        LEFT JOIN {self.users} t on t.id = m.trainer_id
                        WHERE u.role_id = 1'''
        return await fetch_all(get_query)

    async def get_all_users1(self, user_id: str) -> List[dict]:
        get_query = f'''SELECT u.id, concat(u.first_name, ' ', u.last_name) as Name,  u.email, u.phone, m.trainer_id ,
                        concat(t.first_name, ' ', t.last_name) as trainer_name  FROM  {self.users} u 
                        LEFT JOIN {self.mapping} m on m.user_id= u.id 
                        LEFT JOIN {self.users} t on t.id = m.trainer_id
                        WHERE u.role_id = $1'''
        return await fetch_all(get_query, user_id)


    async def add_user(self, input_data: UserDataRequest) -> List[dict]:
        query = f'''INSERT INTO {self.users} (first_name, last_name, email, phone, role_id, created_at)
                        values ($1, $2, $3, $4, $5, $6)'''
        query_params = [input_data.first_name, input_data.last_name, input_data.email, input_data.phone,
                        input_data.role_id, int(datetime.now().timestamp()) ]
        return await insert( query, *query_params)


    async def delete_user(self, user_id: int) -> List[dict]:
        query = f'''Delete from {self.users} where id = $1'''

        return await update( query, user_id)


    async def get_users_by_trainer_id(self, trainer_email: str) -> List[dict]:
        query = f'''select u.id, concat(u.first_name, ' ', u.last_name) as Name,  u.email, u.phone from {self.users} u 
                    where id in (select user_id from {self.mapping}  where trainer_id = (
                    select id from {self.users} where email = $1
                     ))'''

        return await fetch_all( query, trainer_email)

    async def get_exercise_types(self) -> List[dict]:
        query = f'''select * from {self.exercise_types} order by name '''
        return await fetch_all( query)



    async def add_exercise_type(self, input_data: ExerciseDataRequest) -> List[dict]:
        query = f'''INSERT INTO {self.exercise_types} (name)
                        values ($1)'''
        query_params = [input_data.name]
        return await insert( query, *query_params)


    async def delete_exercise_type(self, type_id: int) -> List[dict]:
        query = f'''delete from {self.exercise_types} where id = $1 '''
        return await update( query, type_id)

    async def add_super_set(self, input_data: SuperSetDataRequest) -> List[dict]:
        query = f'''INSERT INTO {self.exercise_types} (name)
                        values ($1)'''
        query_params = [input_data.name]
        return await insert( query, *query_params)

    async def insert_superset_and_exercises(self, input_data: SuperSetDataRequest):
        """
        Inserts superset info and corresponding exercise details in a transaction.
        Returns:
            dict: Result of the operation.
        """
        superset_query = f"""
            INSERT INTO {self.super_sets} (super_set_name, user_id, trainer_id, session_date)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """

        exercise_query = f"""
            INSERT INTO {self.exercise} (super_sets_id, exercise_type_id, reps, weight)
            VALUES ($1, $2, $3, $4)
        """

        try:
            async with connection_pool.acquire() as conn:
                async with conn.transaction():
                    # Insert superset and get its ID
                    superset_id = await conn.fetchval(
                        superset_query,
                        input_data.name,
                        input_data.user_id,
                        input_data.trainer_id,
                        input_data.session_time
                    )

                    # Insert exercise details using the superset ID
                    for exercise in input_data.exercise_details:
                        await conn.execute(
                            exercise_query,
                            superset_id,
                            exercise.exercise_id,
                            exercise.reps,
                            exercise.weight
                        )
            return {"message": "Superset and exercises inserted successfully", "superset_id": superset_id}
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            raise e

