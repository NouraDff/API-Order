import os
import click   
import sqlite3 
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, AutoField, CharField, IntegerField, BooleanField

def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())
    
class Product(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    in_stock = BooleanField()
    description = CharField()
    price = IntegerField()
    image = CharField() 

    def __str__(self):
        return self.name

@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.create_tables([Product])
    click.echo("Initialized the database")

def init_app(app):
    app.cli.add_command(init_db_command)
