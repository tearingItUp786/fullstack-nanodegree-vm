import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, Enum

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    # table columns
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    id = Column(Integer, primary_key=True)


class Puppy(Base):
    __tablename__ = 'puppy'
    # columns
    name = Column(String(80), nullable=False)
    dateOfBirth = Column(Date)
    gender = Column(Enum("male", "female", name='gender'),
                    nullable=False)
    weight = Column(Numeric(10))
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    id = Column(Integer, primary_key=True)

engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
