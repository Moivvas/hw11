from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase


async def get_contacts(db: Session, user: User):
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user_id of the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter_by(user_id=user.id).all()
    return contacts


async def get_contact_by_id(id: int, user_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=id, user_id=user_id).first()
    return contact


async def get_contact_by_email(email: str, user_id: int, db: Session):
    contact = db.query(Contact).filter_by(email=email, user_id=user_id).first()
    return contact


async def create(body: ContactBase, db: Session, user: User):
    """
    The create function creates a new contact in the database.
        
    
    :param body: ContactBase: Pass in the data from the request body
    :param db: Session: Access the database
    :param user: User: Get the user id of the current logged in user
    :return: The contact object
    :doc-author: Trelent
    """
    contact = Contact(**body, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(id: int, body: ContactBase, user_id: int, db: Session):
    """
    The update function updates a contact in the database.
        
    :param id: int: Identify the contact that will be updated
    :param body: ContactBase: Get the data from the request body
    :param user_id: int: Check if the contact belongs to the user
    :param db: Session: Access the database
    :return: A contact
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(id, db)
    if contact and contact.user_id == user_id:
        if body.email:
            contact.email = body.email
        if body.additional_data:
            contact.additional_data = body.additional_data
        if body.birth_date:
            contact.birth_date = body.birth_date
        db.commit()
    return contact



async def remove(id: int, user_id: int, db: Session):
    """
    The remove function removes a contact from the database.
        
    
    :param id: int: Specify the id of the contact to be deleted
    :param user_id: int: Check if the user is authorized to delete the contact
    :param db: Session: Pass the database session to the function
    :return: A contact object if it exists, otherwise none
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(id, db)
    if contact and contact.user_id == user_id:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthdays(start_date: date, end_date: date, db: Session, user: User):
    birthdays = (
        db.query(Contact)
        .filter(Contact.birth_date >= start_date, Contact.birth_date <= end_date, Contact.user_id == user.id)
        .all()
    )
    return birthdays


async def search_contacts_by_last_name(last_name: str, db: Session, user: User):
    contacts = db.query(Contact).filter_by(last_name=last_name, user_id=user.id).all()
    return contacts


async def search_contacts_by_first_name(first_name: str, db: Session, user: User):
    contacts = db.query(Contact).filter_by(first_name=first_name, user_id=user.id).all()
    return contacts


async def search_contact_by_email(email: str, db: Session, user: User):
    contact = db.query(Contact).filter_by(email=email, user_id=user.id).first()
    return contact