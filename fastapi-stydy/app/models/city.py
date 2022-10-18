from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, MetaData, String, Table, func
from sqlalchemy.orm import relationship
# from .base import Base
from sqlalchemy.ext.declarative import declarative_base

from .base import Base
from app.database import engine


class City(Base):
    __tablename__ = 'city'   # 表名
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)   # id
    provience = Column(String(30))  # 省份
    country = Column(String(30))  # 国家
    country_population = Column(BigInteger)  # 国家人口
    data = relationship('Data', back_populates='city')  # Data 是关联的类名，back_populates 是反向访问的属性名
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    name = Column(String(20))

    def __repr__(self) -> str:
        return f'{self.country}-{self.provience}'

class Data(Base):
    __tablename__ = 'data'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # id
    city_id = Column(Integer, ForeignKey('city.id'))  # 映射的是 city表中的id属性
    date = Column(DateTime, nullable=False)
    conformed = Column(Integer, nullable=False, default=0)
    deaths = Column(Integer, nullable=False, default=0)
    recovered = Column(Integer, nullable=False, default=0)
    city = relationship('City', back_populates='data')  # city 是一对多的关联


    def __repr__(self) -> str:
        return f'{self.id}'


