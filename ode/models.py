"""
ode.models module
"""
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    status = Column(String)
    price = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    sq_ft = Column(Integer)
    geom = Column(Geometry('POINT', srid=4326))
