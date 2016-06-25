from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_model import Base, Shelter, Puppy
import datetime


engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def query_one():

    result = session.query(Puppy.name).order_by(Puppy.name.asc()).all()

    for item in result:
        print item[0]

# Query all of the puppies that are less than 6 months old
# organized by the youngest first


def query_two():
    current_date = datetime.date.today()
    six_months_ago = current_date - datetime.timedelta(days=183)

    result = session.query(Puppy.name, Puppy.dateOfBirth).filter(
        Puppy.dateOfBirth >= six_months_ago
    ).order_by(Puppy.dateOfBirth.desc()).all()

    for item in result:
        print item[0], item[1]


def query_three():
    result = session.query(Puppy.name, Puppy.weight).order_by(
        Puppy.weight.asc()).all()

    for item in result:
        print item[0], item[1]


def query_four():
    result = session.query(Shelter, func.count(Puppy.id)).join(
        Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]
# query_one()
# query_two()
# query_three()
query_four()
