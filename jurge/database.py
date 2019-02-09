import alembic.config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
import pkg_resources
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()
session = None


def init(db_url):
    global session
    global Base
    engine = create_engine(db_url)
    session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    Base.query = session.query_property()
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


def migrate():
    connection = session.connection()
    config = _get_alembic_config()
    script_directory = ScriptDirectory.from_config(config)
    context = EnvironmentContext(config, script_directory)
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        fn=lambda rev, context: script_directory._upgrade_revs('head', rev))
    context.run_migrations()
    session.commit()


def _get_alembic_config():
    config_file_name = pkg_resources.resource_filename(
        'jurge', 'alembic/alembic.ini')
    return alembic.config.Config(config_file_name)
