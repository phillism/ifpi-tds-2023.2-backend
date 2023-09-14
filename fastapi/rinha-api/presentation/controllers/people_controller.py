from typing import Optional
from fastapi import APIRouter, HTTPException
from application.user_service import PersonService
from presentation.models.person_model import Person, PersonInput

router = APIRouter(
    prefix="/pessoas", 
    tags=["people"],
)

person_service = PersonService()

@router.get('/', status_code=200)
def get_people(t: Optional[str] = None):
    if t:
        return person_service.search_persons(t)
    
    return person_service.get_people()

@router.get('/{person_id}', status_code=200)
def get_person(person_id):
    found_person = person_service.find_person_by_id(person_id)

    if not found_person:
        raise HTTPException(404, f"There's no one registred with ID '{person_id}'.")
    
    return found_person

@router.post('/', status_code=201)
def add_people(input_person: PersonInput) -> Person:
    created_person = person_service.create_person(Person(
        apelido=input_person.apelido, 
        nome=input_person.nome, 
        nascimento=input_person.nascimento,
        stack=input_person.stack
    ))
    
    return created_person
