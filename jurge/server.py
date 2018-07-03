from flask import Flask

from flask_graphql import GraphQLView

from . import database, graphql


app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.session.remove()


@app.route('/')
def root():
    return 'Hello world'


def run():
    database.init()
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql', schema=graphql.schema, graphiql=True))
    app.run()
