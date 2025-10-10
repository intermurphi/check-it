from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    desc: str
    status: bool