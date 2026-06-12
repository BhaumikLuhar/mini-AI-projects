from pydantic import BaseModel, EmailStr, EmailStr, Field
from typing import List

class CRMLookupInput(BaseModel):
    email: str = Field(min_length=5, max_length=255)

class InventoryInput(BaseModel):
    sku: str = Field(min_length=3, max_length=50)

class QuoteItem(BaseModel):
    sku: str
    quantity : int = Field(gt=0)

class QuoteInput(BaseModel):
    items: List[QuoteItem]
    discount_tier:str = Field(pattern="^(bronze|silver|gold|platinum)$")

class EmailDraftInput(BaseModel):
    recipient_name: str
    recipient_email: EmailStr
    company: str
    context: str

class SearchInput(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=500
    )

class ListInventoryInput(BaseModel):
    pass

class FindProductInput(BaseModel):
    keyword: str