#!python/bin/python
from app import models, db
from config import ROLE_USER

user = models.User('admin', 'admin@example.com', 'harnetly365')
user.set_role(ROLE_USER['admin'])

db.session.add(user)
db.session.commit()

print('User admin successfully created.')
