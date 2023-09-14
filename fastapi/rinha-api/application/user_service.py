import uuid
from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlmodel import Session, select
from persistence.utils import get_engine
from presentation.models.person_model import Person


class PersonService():

    def __init__(self):
        self.session = Session(get_engine())
    
    def get_people(self):
        query = select(Person)
        people = self.session.exec(query).fetchall()
        self.session.close()
        return people

    def find_person_by_id(self, id: uuid.UUID) -> Person:
        query = select(Person).where(Person.id == id)
        found_person = self.session.exec(query).first()
        self.session.close()
        return found_person
    
    def find_person_by_nickname(self, apelido: str):
        query = select(Person).where(Person.apelido == apelido)
        found_person = self.session.exec(query).first()
        self.session.close()
        return found_person

    def create_person(self, person: Person) -> Person:
        if any(len(s) >= 32 for s in person.stack):
            raise HTTPException(429, "Stack's list should contain names less or equals to 32 characters.")

        if isinstance(person, Person) and self.find_person_by_id(person.id):
            raise HTTPException(429, "Person must have unique IDs, try again with another ID.")

        if self.find_person_by_nickname(person.apelido):
            raise HTTPException(429, f"The nickname {person.apelido} is unavailable.")

        self.session.add(person)
        self.session.commit()
        self.session.refresh(person)
        self.session.close()
        return person

    # Get all persons who has the pasased "querySearch" included
    # at "apelido", "nome" or even "stack" (included in the array).
    # It returns the first found 50 people.
    def search_persons(self, querySearch: str) -> list[Person]:
        querySearch = querySearch.lower()

        ilike = lambda attr:attr.like(f"%{querySearch}%")
        
        query = select(Person).where(or_(
            ilike(Person.nome),
            ilike(Person.apelido),
            ilike(Person.stack),
        ))
        
        found_people = self.session.exec(query).fetchmany(50)
        self.session.close()
        return found_people

    def count_people(self) -> int:
        pass
