from dataclasses import dataclass

from mashumaro import DataClassDictMixin
from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str
    icon: str


class SubcategoryIn(CategoryIn):
    category_id: int


@dataclass
class CategoryInternal(DataClassDictMixin):
    category_id: int
    name: str
    icon: str


@dataclass
class SubcategoryInternal(DataClassDictMixin):
    subcategory_id: int
    category_id: int
    name: str
    icon: str
