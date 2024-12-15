from fastapi import APIRouter, Depends
from app.dependencies.gym_depencies import get_gym_service
from app.services.gym_service import GymService
from app.models.gym import UserDataRequest

gym_router = APIRouter(prefix="/gym", tags=["Gym"])


@gym_router.get("/get_all_users")
async def get_members(service: GymService = Depends(get_gym_service)):
    print("Router loaded successfully")
    return await service.fetch_all_members()


@gym_router.post("/add_user")
async def add_user(input_data: UserDataRequest, service: GymService = Depends(get_gym_service)):
    # print("Input data:", input_data.model_dump())  # To check input_data
    return await service.add_user(input_data)

@gym_router.delete("/delete_user")
async def delete_user(user_id: int, service: GymService = Depends(get_gym_service)):
    # print("Input data:", input_data.model_dump())  # To check input_data
    return await service.delete_user(user_id)


@gym_router.get("/get_users_by_trainer_id")
async def get_users_by_trainer(trainer_email: str, service: GymService= Depends(get_gym_service)):
    return await service.get_users_by_trainer_id(trainer_email)

