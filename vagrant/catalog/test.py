from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


def result_query():
    query = session.query(Restaurant).all()
    return query


def search_for_existing(a_restaurant_name):
    query = session.query(Restaurant.name).filter(
        Restaurant.name == a_restaurant_name).all()
    return query


def search_by_id(id):
    a_restaurant = session.query(Restaurant).filter_by(id=id).first()
    print a_restaurant
    if a_restaurant:
        return a_restaurant
    else:
        return None


def list_of_restaurant_items(a_restaurant):
    list_of_items = session.query(MenuItem).filter_by(
        restaurant_id=a_restaurant.id)
    return list_of_items


def insert_new(name):
    a_restaurant = Restaurant(name=name)
    session.add(a_restaurant)
    session.commit()
    return


def update_name(id, new_name):
    a_restaurant = search_by_id(id)
    if a_restaurant:
        a_restaurant.name = new_name
        session.add(a_restaurant)
        session.commit()
    return


def delete_entry(id):
    a_restaurant = search_by_id(id)
    if a_restaurant:
        session.delete(a_restaurant)
        session.commit()
        return True
    else:
        return None
