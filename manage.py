#!/usr/bin/env python
import os

from app import create_app, db
from app.models import User, Interest
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Interest': Interest
    }
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def bootstrap():
    """ Create database with fake data """
    db.create_all()
    os.environ['ADMIN_EMAIL'] = 'osadchuk.m.01@gmail.com'
    os.environ['ADMIN_PASSWORD'] = '1111'
    admin = User(email='osadchuk.m.01@gmail.com', username='Maxim', password='1111')
    admin.gravatar()
    db.session.commit()
    db.session.add(admin)
    User._bootstrap()
    Interest._bootstrap()


if __name__ == '__main__':
    manager.run()
