from typing import List
from datetime import date, timedelta

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactBase


router = APIRouter(prefix="/contacts", tags=["contacts"])

# need to add "skip limit"


@router.get("/", response_model=List[ContactResponse], name="Return contacts")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/search_by_id/{id}", response_model=ContactResponse)
async def get_contact(id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_last_name/{last_name}",
    response_model=List[ContactResponse],
    name="Search contacts by last name",
)
async def search_contacts_by_last_name(last_name: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_contacts_by_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_first_name/{first_name}",
    response_model=List[ContactResponse],
    name="Search contacts by first name",
)
async def search_contacts_by_first_name(first_name: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_contacts_by_first_name(first_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_email/{email}",
    response_model=List[ContactResponse],
    name="Search contacts by email",
)
async def search_contacts_by_email(email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.search_contact_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contacts(body: ContactBase, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is exists!"
        )

    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{id}", response_model=ContactResponse)
async def update_contact(body: ContactBase, id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update(id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/birthdays", response_model=List[ContactResponse], name="Upcoming Birthdays"
)
async def get_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    birthdays = await repository_contacts.get_birthdays(today, end_date, db)
    if birthdays is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return birthdays
