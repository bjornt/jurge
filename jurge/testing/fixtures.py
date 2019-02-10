import pytest

from pytest_postgresql import factories as pg_factory

from .. import database


@pytest.fixture
def session(postgresql_proc):
    db_name = 'unittests'
    port = postgresql_proc.port
    user = postgresql_proc.user
    socketdir = postgresql_proc.unixsocketdir
    pg_factory.init_postgresql_database(user, socketdir, port, db_name)
    db_url = (
        f'postgresql:///{db_name}?'
        f'user={user}&host={socketdir}&port={port}')
    database.init(db_url)
    database.migrate()
    yield database.session
    pg_factory.drop_postgresql_database(
        user, socketdir, port, db_name, postgresql_proc.version)
