import graphene
from werkzeug.exceptions import default_exceptions, BadRequest


class Query(graphene.ObjectType):

    hello = graphene.String(
        name=graphene.String(
            default_value="stranger",
            description='Name of the person to be greeted'),
        description='Returns a greeting for the specified person')

    def resolve_hello(self, info, name):
        return 'Hello ' + name

    error = graphene.String(
        code=graphene.Int(default_value=400),
        description='Returns the specified HTTP error')

    def resolve_error(self, info, code):
        if code not in default_exceptions:
            raise BadRequest('Unsupported error code {}'.format(code))
        raise default_exceptions[code]


class Mutations(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)  # , mutation=Mutations
