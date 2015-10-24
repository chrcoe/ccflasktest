#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from flask_migrate import MigrateCommand
from flask.ext.login import login_required, make_secure_token, get_auth_token

from ccflasktest.app import create_app
from ccflasktest.user.models import User
from ccflasktest.settings import DevConfig, ProdConfig
from ccflasktest.database import db

if os.environ.get("CCFLASKTEST_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


@app.route('/token', methods=['POST'])
#  @login_required
def get_token():
    # this will make a secure token based on the current user's ID
    # cannot get a token without being first logged in...
    # maybe we want to accept username/password for every POST /token
    # and then validate the user.  If valid, then return token ?
    #  return make_secure_token(current_user.id)
    return get_auth_token()
    #  s = Serializer(app.config['SECRET_KEY'], expires_in=600)
    #  return s.dumps({'id': current_user.id})

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    manager.run()
