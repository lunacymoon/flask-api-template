from pydantic import BaseModel, constr


class BookSchema(BaseModel):
    id: int
    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)

    class Config:
        orm_mode = True
