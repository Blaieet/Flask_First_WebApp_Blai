from flask_script import Manager
from fooApp.app import app

manager = Manager(app)
app.config['DEBUG'] = False # Ensure debugger will load.

if __name__ == '__main__':
    manager.run()