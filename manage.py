# manage.py
import os
import unittest

from flask_script import Manager

from app import app

app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)

# migrations


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == '__main__':
    manager.run()
