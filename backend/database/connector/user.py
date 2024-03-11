"""
Database connector for UserDB class
"""
from sqlalchemy.exc import SQLAlchemyError

from database import Session
from database.schema import UserDB
from database.models import CreateEntryResponse, UpdateEntryResponse, DeleteEntryResponse

from typing import Optional
from datetime import datetime
def create_user_in_db(
        username: str, email: str, password: str, salt: str,
        created_by: str, profile_picture: Optional[str] = None,
        first_name: Optional[str] = None, last_name: Optional[str] = None,
        birthday: Optional[datetime] = None, return_id: bool = False) \
        -> CreateEntryResponse:
    session = Session()
    try:
        new_user = UserDB(
                    username=username,
                    email=email,
                    password=password,
                    salt=salt,
                    created_by=created_by,
                    updated_by=created_by,
                    profile_picture=profile_picture,
                    first_name=first_name,
                    last_name=last_name,
                    birthday=birthday
                )
        session.add(new_user)
        session.commit()
        created_id = new_user.id
        session.close()

        if return_id:
            return CreateEntryResponse(
                success=True,
                created_id=created_id
            )
        else:
            return CreateEntryResponse(
                success=True
            )

    except SQLAlchemyError as e:
        session.rollback()
        return CreateEntryResponse(
            success=False,
            error=str(e)
        )


def get_user_in_db_by_username(username: str) -> UserDB | None:
    session = Session()
    query = session.query(UserDB).filter(UserDB.username == username).first()
    session.close()
    return query


def get_user_in_db_by_email(email: str) -> UserDB | None:
    session = Session()
    query = session.query(UserDB).filter(UserDB.email == email).first()
    session.close()
    return query


def update_user_in_db(
        user_id: int, updated_by: str, username: Optional[str] = None,
        email: Optional[str] = None, password: Optional[str] = None,
        profile_picture: Optional[str] = None, first_name: Optional[str] = None,
        last_name: Optional[str] = None, birthday: Optional[datetime] = None) \
        -> UpdateEntryResponse:

    session = Session()
    try:
        update_dict = {"updated_by": updated_by}
        if username is not None:
            update_dict["username"] = username
        if email is not None:
            update_dict["email"] = email
        if password is not None:
            update_dict["password"] = password
        if profile_picture is not None:
            update_dict["profile_picture"] = profile_picture
        if first_name is not None:
            update_dict["first_name"] = first_name
        if last_name is not None:
            update_dict["last_name"] = last_name
        if birthday is not None:
            update_dict["birthday"] = birthday

        session.query(UserDB).filter(UserDB.id == user_id).update(update_dict)
        session.commit()
        return UpdateEntryResponse(success=True)

    except SQLAlchemyError as e:
        session.rollback()
        return UpdateEntryResponse(
            success=False,
            error=str(e)
        )


def delete_user_in_db(user_id: int) -> DeleteEntryResponse:
    session = Session()
    try:
        success = session.query(UserDB).filter(UserDB.id == user_id).delete(synchronize_session="fetch")
        session.commit()
        session.close()
        if success:
            return DeleteEntryResponse(success=True)
        else:
            return DeleteEntryResponse(success=False)

    except SQLAlchemyError as e:
        session.rollback()
        return DeleteEntryResponse(
            success=False,
            error=str(e)
        )