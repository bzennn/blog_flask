#!python/bin/python
from app import db
from config import SQLALCHEMY_DATABASE_URI

db.create_all()
db.session.commit()
print('Database successfully created on ' + SQLALCHEMY_DATABASE_URI)
