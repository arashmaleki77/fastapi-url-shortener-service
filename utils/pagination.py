from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from fastapi import Request


class PaginationMeta(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    next_page: Optional[str] = None
    previous_page: Optional[str] = None


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: PaginationMeta


class PaginationManager:
    def __init__(self, query, page: int, page_size: int, request: Request, schema):
        self.query = query
        self.page = page
        self.page_size = page_size
        self.request = request
        self.schema = schema

    def paginate(self):
        new_pagination_meta = self.get_pagination_meta()
        offset = self.page_size * (self.page - 1)
        paginated_query = list(self.query)[offset:offset+self.page_size]
        result = []
        for item in paginated_query:
            result.append(self.schema.model_validate(item[0]))
        return PaginatedResponse(items=result, meta=new_pagination_meta)

    def get_pagination_meta(self):
        total_items = len(self.query)
        total_pages = (total_items + self.page_size - 1) // self.page_size
        next_page, previous_page = self.create_pagination_links(total_pages)
        return PaginationMeta(
            total_items=total_items, total_pages=total_pages, current_page=self.page, page_size=self.page_size,
            next_page=next_page, previous_page=previous_page
        )

    def create_pagination_links(self, total_pages: int):
        base_url = str(self.request.url).split("?")[0]
        next_page = f"{base_url}?page={self.page + 1}&page_size={self.page_size}" if self.page < total_pages else None
        previous_page = f"{base_url}?page={self.page - 1}&page_size={self.page_size}" if self.page > 1 else None
        return next_page, previous_page
