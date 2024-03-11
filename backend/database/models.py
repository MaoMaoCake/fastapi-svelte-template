"""
Database CRUD models
"""
from typing import Optional
from pydantic import BaseModel


class CreateEntryResponse(BaseModel):
    """
    Return class for creating entries
    """
    success: bool
    error: Optional[str]
    created_id: int


class UpdateEntryResponse(BaseModel):
    """
    Return class for Updating entries
    """
    success: bool
    error: Optional[str]


class DeleteEntryResponse(BaseModel):
    """
    Return class for Deleting entries
    """
    success: bool
    error: Optional[str]
