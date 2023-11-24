from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserBase


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserBase, db: Session):
    """
    The create_user function creates a new user in the database.
        
    
    :param body: UserBase: Pass the data from the request into this function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    g = Gravatar(body.email)

    new_user = User(**body.model_dump(), avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()
    
async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    
async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    Args:
        email (str): The email address of the user to update.
        url (str): The URL for the new avatar image.
        db (Session, optional): A database session object to use instead of creating one locally. Defaults to None.  # noQA: E501 line too long
    
    :param email: Get the user by email
    :param url: str: Specify the type of data that will be passed to the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
