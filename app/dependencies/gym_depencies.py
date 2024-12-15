from app.queries.gym_queries import GymQuery
from app.services.gym_service import GymService

def get_gym_service()-> GymService:
    query = GymQuery()
    return  GymService(query)