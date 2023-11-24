from typing import List
from datetime import date, timedelta


from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactBase, UserBase, UserResponse
from src.services.auth import auth_service



router = APIRouter(prefix="/contacts", tags=["contacts"])

# need to add "skip limit"


@router.get("/", response_model=List[ContactResponse], name="Return contacts")

async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.
        
    
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(db, current_user)
    return contacts


@router.get("/search_by_id/{id}", response_model=ContactResponse)
async def get_contact(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
        Args:
            id (int): The ID of the contact to return.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object from auth_service.get_current_user(). Defaults to Depends(auth_service.get_current_user).
        Returns:
            Contact: A single Contact object matching the specified ID.
    
    :param id: int: Specify the type of data that will be passed in
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact



@router.get(
    "/search_by_last_name/{last_name}",
    response_model=List[ContactResponse],
    name="Search contacts by last name",
)
async def search_contacts_by_last_name(last_name: str, db: Session = Depends(get_db),
                                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts_by_last_name(last_name, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_first_name/{first_name}",
    response_model=List[ContactResponse],
    name="Search contacts by first name",
)
async def search_contacts_by_first_name(first_name: str, db: Session = Depends(get_db),
                                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts_by_first_name(first_name, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/search_by_email/{email}",
    response_model=List[ContactResponse],
    name="Search contacts by email",
)
async def search_contacts_by_email(email: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    """
    The search_contacts_by_email function searches for a contact by email.
        Args:
            email (str): The email of the contact to search for.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth_service module's get_current_user function. 
                Defaults to Depends(auth_service.get_current_user).
    
    :param email: str: Specify the email of the contact we want to search for
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user_id of the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.search_contact_by_email(email, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contacts(body: ContactBase, db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contacts function creates a new contact in the database.
        Args:
            body (ContactBase): The contact to create.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
    
    :param body: ContactBase: Get the contact information from the request body
    :param db: Session: Pass in the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(body.email, db, current_user)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists!"
        )

    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{id}", response_model=ContactResponse)
async def update_contact(body: ContactBase, id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as parameters, which are used to update the contact.
        If no contact is found with that id, then an HTTPException is raised.
    
    :param body: ContactBase: Pass the data from the request body to the function
    :param id: int: Identify the contact to be updated
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            id (int): The ID of the contact to remove.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The currently authenticated user object for authorization purposes. Defaults to Depends(auth_service.get_current_user).
        Returns:
            Contact: A Contact object representing the removed contact.
    
    :param id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the auth_service
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove(id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get(
    "/birthdays", response_model=List[ContactResponse], name="Upcoming Birthdays"
)
async def get_birthdays(db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_birthdays function returns a list of contacts with birthdays in the next 7 days.
        The function takes two parameters:
            - db: A database connection object, which is passed by default from the get_db() function.
            - current_user: An authenticated user object, which is passed by default from the auth_service.get_current_user() function.
    
    :param db: Session: Get the database connection
    :param current_user: User: Get the current user from the database
    :return: A list of contacts that have a birthday in the next 7 days
    :doc-author: Trelent
    """
    today = date.today()
    end_date = today + timedelta(days=7)
    birthdays = await repository_contacts.get_birthdays(today, end_date, db, current_user)
    if birthdays is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return birthdays
