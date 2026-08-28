from fastapi import APIRouter
from app.pets.pets_schemas import CreatePetDto, Pet, UpdatePetDto
from app.pets.pets_service import pets_service
from app.students.students_schemas import StandardResponse

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)

@router.get("", response_model=StandardResponse)
def find_all(studentId: str):
    pets = pets_service.find_all_for_student(studentId)
    return {
        "success": True,
        "status": 200,
        "message": "Mascotas obtenidas exitosamente",
        "data": pets
    }

@router.post("", status_code=201, response_model=StandardResponse)
def create(studentId: str, body: CreatePetDto):
    new_pet = pets_service.create(studentId, body)
    return {
        "success": True,
        "status": 201,
        "message": "Mascota creada exitosamente",
        "data": new_pet
    }

@router.patch("/{petId}", response_model=StandardResponse)
def update(studentId: str, petId: str, body: UpdatePetDto):
    updated_pet = pets_service.update(studentId, petId, body)
    return {
        "success": True,
        "status": 200,
        "message": "Mascota actualizada exitosamente",
        "data": updated_pet
    }

@router.delete("/{petId}", response_model=StandardResponse)
def delete(studentId: str, petId: str):
    deleted_pet = pets_service.delete(studentId, petId)
    return {
        "success": True,
        "status": 200,
        "message": "Mascota eliminada exitosamente",
        "data": deleted_pet
    }
