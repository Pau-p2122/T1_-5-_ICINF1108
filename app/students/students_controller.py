from fastapi import APIRouter, HTTPException, status
from app.students.students_service import StudentService
from app.students.students_schemas import StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])
service = StudentService()

@router.get("")
def get_students():
    students = service.get_all()
    return {
        "success": True,
        "status": 200,
        "message": "Estudiantes obtenidos exitosamente",
        "data": students
    }

@router.get("/{student_id}")
def get_student(student_id: str):
    student = service.get_by_id(student_id)
    if not student:
        return {
            "success": False,
            "status": 404,
            "message": "Estudiante no encontrado",
            "data": None
        }
    return {
        "success": True,
        "status": 200,
        "message": "Estudiante encontrado",
        "data": student
    }

@router.post("", status_code=201)
def create_student(student_data: StudentCreate):
    new_student = service.create(student_data)
    return {
        "success": True,
        "status": 201,
        "message": "Estudiante creado exitosamente",
        "data": new_student
    }

@router.put("/{student_id}")
def update_student(student_id: str, student_data: StudentUpdate):
    updated_student = service.update(student_id, student_data)
    if not updated_student:
        return {
            "success": False,
            "status": 404,
            "message": "No se pudo actualizar, estudiante no encontrado",
            "data": None
        }
    return {
        "success": True,
        "status": 200,
        "message": "Estudiante actualizado exitosamente",
        "data": updated_student
    }

@router.delete("/{student_id}")
def delete_student(student_id: str):
    deleted = service.delete(student_id)
    if not deleted:
        return {
            "success": False,
            "status": 404,
            "message": "No se pudo eliminar, estudiante no encontrado",
            "data": None
        }
    return {
        "success": True,
        "status": 200,
        "message": "Estudiante eliminado exitosamente",
        "data": None
    }