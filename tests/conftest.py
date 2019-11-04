import os
import tempfile

os.environ['DATABASE'] = ":memory:"

import pytest
from peewee import SqliteDatabase

from inf5190 import create_app
from inf5190.models import get_db_path, Product, Order

@pytest.fixture
def app():
    app = create_app({"TESTING" : True})

    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, Order])

    yield app

    database.drop_tables([Product, Order])

@pytest.fixture
def client(app):
    return app.test_client()