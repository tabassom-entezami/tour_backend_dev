from sqlite3 import Connection as SQLite3Connection

import pytest
from nameko.testing.services import worker_factory
from sqlalchemy import event
from sqlalchemy.engine import Engine

from tour_shared.models import DeclarativeBase


@pytest.fixture(scope='session')
def db_url():
    return 'sqlite:///:memory:'


@pytest.fixture(scope='session')
def model_base():
    return DeclarativeBase


@pytest.fixture(scope='session')
def db_engine_options():
    # NOTE: Sqlite does not support foreign key constraint by default for
    # backward compatibility. It must be enabled manually.
    @event.listens_for(Engine, 'connect')
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()

    return {}


@pytest.fixture
def processor(database, mem_store):
    # local import will help avoid Configuration error during test
    # since config_translate fixture needs a chance to run before we hit
    # a gettext invocation ( check the commit)
    from processor.controller import ProcessorController
    return worker_factory(
        ProcessorController,
        db=database,
        mem_store=mem_store,
    )


@pytest.fixture
def access_info():
    return {
        'is_admin': False,
        'language': 'en',
        'user': {
            'id': 'long-uuid',
        }
    }
