from fastapi import APIRouter

from app.pets.pets_schemas import CreatePetDto, Pet, UpdatePetDto
from app.pets.pets_service import pets_service
from app.shared.response import ApiResponse

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)


@router.get("")
def find_all(studentId: str) -> ApiResponse[list[Pet]]:
    pets = pets_service.find_all_for_student(studentId)

    return ApiResponse(
        success=True,
        status=200,
        message="Mascotas obtenidas correctamente",
        data=pets
    )


@router.post("", status_code=201)
def create(
    studentId: str, body: CreatePetDto
) -> ApiResponse[Pet]:
    pet = pets_service.create(studentId, body)

    return ApiResponse(
        success=True,
        status=201,
        message="Mascota creada correctamente",
        data=pet
    )


@router.patch("/{petId}")
def update(
    studentId: str, petId: str, body: UpdatePetDto
) -> ApiResponse[Pet]:
    pet = pets_service.update(studentId, petId, body)

    return ApiResponse(
        success=True,
        status=200,
        message="Mascota actualizada correctamente",
        data=pet
    )


@router.delete("/{petId}")
def delete(studentId: str, petId: str) -> ApiResponse[Pet]:
    deleted = pets_service.delete(studentId, petId)

    return ApiResponse(
        success=True,
        status=200,
        message="Mascota eliminada correctamente",
        data=deleted
    )
