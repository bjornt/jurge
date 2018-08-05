from flask import Flask

from flask_graphql import GraphQLView

from . import database, graphql

app = None


def create_app():
    new_app = Flask(__name__, static_folder='build')
    database.init()
    new_app.add_url_rule(
        '/api/graphql',
        view_func=GraphQLView.as_view(
            'graphql', schema=graphql.schema, graphiql=True))

    @new_app.teardown_appcontext
    def shutdown_session(exception=None):
        database.session.remove()

    @new_app.route('/api')
    def root():
        return 'Hello world'

    global app
    app = new_app
    return app


def run():
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
