import bottle
from bottle import (
    auth_basic,
    request,
    route,
    run,
    ServerAdapter,
    default_app,
)
from beaker.middleware import SessionMiddleware
from bottle.ext.sqlalchemy import SQLAlchemyPlugin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from model import Base
from strategy.cls_raw import Raw

engine = engine = create_engine(
    '{engine}://{username}:{password}@{host}:{port}/{db_name}'.format(
        **settings.COCKROACH
    ),
    echo=settings.SQLALCHEMY['debug']
)
session_local = sessionmaker(
    bind=engine,
    autoflush=settings.SQLALCHEMY['autoflush'],
    autocommit=settings.SQLALCHEMY['autocommit']
)

def setup_routes():
     bottle.route('/pop/<pop_id>', ['GET', 'DELETE'], crud)
     bottle.route('/pop/<pop_name>/<pop_color>', ['PUT'], insert_entry)
     bottle.route('/pop/<pop_id>/<pop_name>/<pop_color>', ['POST'], update_entry)

def is_authenticated_user(user, password):
    # You write this function. It must return
    # True if user/password is authenticated, or False to deny access.
	if user == 'user' and password == 'pass':
		return True
	return False

def get_strategy(db):
     return Raw(db)

@route('/')
def hello(db):
	return {"hello": "world"}

@route('/pop')
@auth_basic(is_authenticated_user)
def get_all(db):
    strategy = get_strategy(db)
    return strategy.all()

@route('/pop/<pop_id>')
@auth_basic(is_authenticated_user)
def crud(db, pop_id):
    strategy = get_strategy(db)
    if request.method == 'GET':
        return strategy.filter_by(pop_id)
    
    return strategy.delete_by(pop_id)

@route('/pop/<pop_name>/<pop_color>')
@auth_basic(is_authenticated_user)
def insert_entry(db, pop_name, pop_color):
    strategy = get_strategy(db)
    return strategy.insert_entry(pop_name, pop_color)

@route('/pop/<pop_id>/<pop_name>/<pop_color>')
@auth_basic(is_authenticated_user)
def update_entry(db, pop_id, pop_name, pop_color):
    strategy = get_strategy(db)
    return strategy.update_entry(pop_id, pop_name, pop_color)

bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=False, create_session = session_local))
class SSLCherootAdapter(ServerAdapter):
    def run(self, handler):
        from cheroot import wsgi
        from cheroot.ssl.builtin import BuiltinSSLAdapter
        import ssl

        server = wsgi.Server((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter("./server.crt", "./server.key")

        try:
            server.start()
        finally:
            server.stop()


# define beaker options
# -Each session data is stored inside a file located inside a
#  folder called data that is relative to the working directory
# -The cookie expires at the end of the browser session
# -The session will save itself when accessed during a request
#  so save() method doesn't need to be called
session_opts = {
    "session.type": "file",
    "session.cookie_expires": True,
    "session.data_dir": "./data",
    "session.auto": True,
}

# Create the default bottle app and then wrap it around
# a beaker middleware and send it back to bottle to run
app = SessionMiddleware(default_app(), session_opts)

setup_routes()

if __name__ == "__main__":
    run(app=app, host="0.0.0.0", port=443, server=SSLCherootAdapter)
