import os
import click
import sqlite3
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, AutoField, CharField, IntegerField, BooleanField, ForeignKeyField
from playhouse.sqlite_ext import *

def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())

class Product(BaseModel):
    id = AutoField(primary_key=True, column_name = "id")
    name = CharField()
    in_stock = BooleanField()
    description = CharField()
    price = IntegerField()
    image = CharField()

class CreditCard(BaseModel):
    id=AutoField(primary_key=True)
    name = CharField()
    number = IntegerField()
    expiration_year = IntegerField()
    cvv = IntegerField()
    expiration_month = IntegerField()

class ShippingInformation(BaseModel):
    id=AutoField(primary_key=True)
    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField()

class Transaction(BaseModel):
    id = AutoField(primary_key=True)
    success = BooleanField()
    amount_charged = IntegerField()

class Order(BaseModel):
    id = AutoField(primary_key=True, column_name = "id")
    total_price = IntegerField()
    email = CharField()
    credit_card = JSONField()
    shipping_information = JSONField()
    paid = BooleanField()
    transaction = JSONField() 
    product = JSONField()
    shipping_price = IntegerField()



@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, CreditCard, ShippingInformation, Transaction, Order])
    click.echo("Initialized the database")

def init_app(app):
    app.cli.add_command(init_db_command)
