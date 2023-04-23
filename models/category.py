from dataclasses import dataclass

from mashumaro import DataClassDictMixin
from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str
    icon: str


@dataclass(kw_only=True)
class CategoryInternal(DataClassDictMixin):
    category_id: int
    name: str
    icon: str
