from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactBase


# need to add "skip limit"


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_id(id: int, db: Session):
    contact = db.query(Contact).filter_by(id=id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def create(body: ContactBase, db: Session):
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(id: int, body: ContactBase, db: Session):
    contact = await get_contact_by_id(id, db)
    if contact:
        contact.email = body.email
        contact.additional_data = body.additional_data
        contact.birth_date = body.birth_date
        db.commit()
    return contact


async def remove(id: int, db: Session):
    contact = await get_contact_by_id(id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthdays(start_date: date, end_date: date, db: Session):
    birthdays = (
        db.query(Contact)
        .filter(Contact.birth_date >= start_date, Contact.birth_date <= end_date)
        .all()
    )
    return birthdays


async def search_contacts_by_last_name(last_name: str, db: Session):
    contacts = db.query(Contact).filter_by(last_name=last_name).all()
    return contacts


async def search_contacts_by_first_name(first_name: str, db: Session):
    contacts = db.query(Contact).filter_by(first_name=first_name).all()
    return contacts


async def search_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).all()
    return contact
