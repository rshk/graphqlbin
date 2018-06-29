import click

from flask import Flask
from flask.cli import FlaskGroup
from flask_graphql import GraphQLView

from .schema import schema


def create_app():

    app = Flask(__name__)

    # @app.errorhandler(401)
    # def handle_401(error):
    #     return Response(str(error), 401, {
    #         'WWWAuthenticate': 'Basic realm="Login Required"',
    #     })

    app.add_url_rule(
        '/graphql',
        view_func=(GraphQLView.as_view(
            'graphql', schema=schema, graphiql=True)))

    # Optional, for adding batch query support (used in Apollo-Client)
    app.add_url_rule(
        '/graphql/batch',
        view_func=(GraphQLView.as_view(
            'graphql-batch', schema=schema, batch=True)))

    # @app.route('/auth', methods=['POST'])
    # def authenticate_user():
    #     username = request.form['username']
    #     password = request.form['password']
    #     user = verify_credentials(username, password)

    #     if user:
    #         token = _create_user_jwt(user)
    #         return json.dumps({'token': token.decode()}), 200, {
    #             'Content-type': 'text/json'}

    #     raise Unauthorized('Bad username / password')

    # CORS(app)

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Wiki application."""
    pass
