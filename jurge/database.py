from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()
#session = None
engine = create_engine('postgresql:///jurge', convert_unicode=True)
session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
Base.query = session.query_property()


def init():
    global session
