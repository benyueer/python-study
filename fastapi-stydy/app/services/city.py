from app.models.city import City
from sqlalchemy.orm.session import Session

from app.schemas.city import CityCreateSchema



def create(payload: CityCreateSchema, session: Session):
    city = City(**payload.dict())

    session.add(city)
    session.commit()
    session.refresh(city)

    return city


def search(offset: int, limit: int, word: str, session: Session):
    query = session.query(City)

    query = query.offset(offset).limit(limit)

    return query.all()