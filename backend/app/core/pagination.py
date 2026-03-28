"""Shared pagination and response utilities — reusable across all routes."""

from __future__ import annotations
from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel
from fastapi import Query
from sqlalchemy.orm import Session, Query as SAQuery
from math import ceil

T = TypeVar("T")


class PaginationParams:
    """Dependency-injectable pagination parameters with sane defaults."""

    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    ):
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: PaginationParams) -> "PaginatedResponse[T]":
        total_pages = ceil(total / params.page_size) if params.page_size > 0 else 0
        return cls(
            items=list(items),
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1,
        )


def paginate_query(query: SAQuery, params: PaginationParams) -> tuple:
    """Apply pagination to a SQLAlchemy query. Returns (items, total_count)."""
    total = query.count()
    items = query.offset(params.offset).limit(params.page_size).all()
    return items, total
