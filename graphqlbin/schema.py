import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return 'Hello ' + name


class Mutations(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)  # , mutation=Mutations
