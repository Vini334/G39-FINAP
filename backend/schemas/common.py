"""
Common Schemas
Shared request and response schemas.
"""

from pydantic import BaseModel
from typing import Any, Optional, List


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    data: Any
    message: Optional[str] = None


class ErrorDetail(BaseModel):
    """Error detail"""
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    data: Optional[Any] = None
    message: str
    errors: List[ErrorDetail] = []


class APIResponse(BaseModel):
    """Generic API response"""
    success: bool
    data: Any = None
    message: Optional[str] = None
    errors: Optional[List[ErrorDetail]] = []
