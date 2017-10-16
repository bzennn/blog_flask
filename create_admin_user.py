#!python/bin/python
from app import models, db
from datetime import datetime
from config import ROLE_USER

user = models.User('admin', 'admin@example.com', 'harnetly365', 'Dmitry', 'Klabukov', datetime.utcnow())
user.set_role(ROLE_USER['admin'])

db.session.add(user)
db.session.commit()

print('User admin successfully created.')
