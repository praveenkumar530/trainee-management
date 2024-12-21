from fastapi import APIRouter, Depends
from app.dependencies.gym_depencies import get_gym_service
from app.services.gym_service import GymService
from app.models.gym import UserDataRequest, ExerciseDataRequest, SuperSetDataRequest

gym_router = APIRouter(prefix="/gym", tags=["Gym"])


@gym_router.get("/get_all_users")
async def get_members(service: GymService = Depends(get_gym_service)):
    return await service.fetch_all_members()


@gym_router.post("/add_user")
async def add_user(input_data: UserDataRequest, service: GymService = Depends(get_gym_service)):
    # print("Input data:", input_data.model_dump())  # To check input_data
    return await service.add_user(input_data)

@gym_router.delete("/delete_user")
async def delete_user(user_id: int, service: GymService = Depends(get_gym_service)):
    return await service.delete_user(user_id)


@gym_router.get("/get_users_by_trainer_email")
async def get_users_by_trainer(trainer_email: str, service: GymService= Depends(get_gym_service)):
    return await service.get_users_by_trainer_id(trainer_email)

@gym_router.get("/get_exercise_types")
async def get_exercise_types( service: GymService= Depends(get_gym_service)):
    return await service.get_exercise_types()


@gym_router.post("/add_exercise_type")
async def add_exercise_type(input_data: ExerciseDataRequest, service: GymService = Depends(get_gym_service)):
    return await service.add_exercise_type(input_data)

@gym_router.delete("/delete_exercise_type")
async def delete_exercise_type(type_id: int, service: GymService = Depends(get_gym_service)):
    return await service.delete_exercise_type(type_id)


@gym_router.post("/add_super_set")
async def add_super_set(input_data: SuperSetDataRequest, service: GymService = Depends(get_gym_service)):
    return await service.add_super_set(input_data)


