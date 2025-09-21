from pydantic import BaseModel
from typing import List, Optional

class JD(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    must_have: Optional[List[str]] = []
    good_to_have: Optional[List[str]] = []