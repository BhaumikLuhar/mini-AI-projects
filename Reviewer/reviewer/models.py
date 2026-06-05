from typing import Literal
from pydantic import BaseModel, Field

class Party(BaseModel):
    name: str   
    role: str

class KeyDate(BaseModel):
    label: str
    date: str

class FlaggedClause(BaseModel):
    clause_type: str
    excerpt: str
    concern: str

    severity: Literal[
        "low",
        "medium",
        "high"
    ]
    
class ReviewReport(BaseModel):
    summary: str

    tldr: list[str] = Field(
        min_length=3,
        max_length=3
    )

    document_type: Literal[
        "NDA",
        "MSA",
        "SOW",
        "Policy",
        "Other"
    ]

    parties: list[Party]

    key_dates: list[KeyDate]

    value_inr: float | None=None

    flagged_clauses: list[FlaggedClause]

    confidence: int =Field(
        ge=0,
        le=100
    )

#chunk schemas
class ChunkParty(BaseModel):
    name: str
    role: str


class ChunkDate(BaseModel):
    label: str
    date: str


class ChunkClause(BaseModel):
    clause_type: str
    excerpt: str
    concern: str
    severity: str


class ChunkAnalysis(BaseModel):
    summary: str

    parties: list[ChunkParty]

    dates: list[ChunkDate]

    clauses: list[ChunkClause]