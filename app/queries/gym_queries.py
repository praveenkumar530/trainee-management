from typing import List
from core.database.database_conn import fetch_all, insert, update
from app.models.gym import UserDataRequest
from datetime import datetime

class GymQuery:

    def __init__(self):
        self.users = "public.users"
        self.mapping = "public.trainer_user_mapping"


    async def get_all_users(self) -> List[dict]:
        get_query = f'''SELECT u.id, concat(u.first_name, ' ', u.last_name) as Name,  u.email, u.phone, m.trainer_id ,
	                    concat(t.first_name, ' ', t.last_name) as trainer_name  FROM  {self.users} u 
                        LEFT JOIN {self.mapping} m on m.user_id= u.id 
                        LEFT JOIN {self.users} t on t.id = m.trainer_id
                        WHERE u.role_id = 1'''
        return await fetch_all(get_query)


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