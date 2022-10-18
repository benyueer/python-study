from pydantic import BaseModel, constr
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class User(BaseModel):
    id: int
    name: str

external_data = {
    "id": 123,
    "name": 'qwe'
}

user = User(**external_data)

# print(user)

Base = declarative_base()

class CompanyOrm(Base):
    __tablename__ = 'companties'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20))

class CompanyModel(BaseModel):
    id: int
    name: constr(max_length=20)  # type: ignore

    class Config:
        orm_mode = True


co_orm = CompanyOrm(
    id=123,
    name='qwe'
)

print(CompanyModel.from_orm(co_orm))
