
import os
import logging

from flask_script import Manager, Server

import app

config_name = os.getenv('FLASK_CONFIG', 'default')
app = app.create_app(config_name)
manager = Manager(app)

if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    manager.add_command('runserver', Server(port=port))

    print("Running %s server on port %s." % (config_name, port))

    if app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG)

    manager.run()
