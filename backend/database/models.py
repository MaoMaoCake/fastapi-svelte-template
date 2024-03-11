from pydantic import BaseModel
from typing import Optional

class CreateEntryResponse(BaseModel):
    success: bool
    error = Optional[str]
    created_id: int

class UpdateEntryResponse(BaseModel):
    success: bool
    error: Optional[str]

class DeleteEntryResponse(BaseModel):
    success: bool
    error : Optional[str]