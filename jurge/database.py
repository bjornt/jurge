from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()
engine = create_engine('postgresql:///jurge', convert_unicode=True)
session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base.query = session.query_property()


def init():
    return session()


def transact(func, *args, **kwargs):
    session()
    try:
        result = func(*args, **kwargs)
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return result
