from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from graphql_server.resolvers.query import query, user
from graphql_server.resolvers.mutation import mutation
from starlette.middleware.cors import CORSMiddleware


class GraphQLServer:

    def __init__(self, debug=True):

        type_defs = load_schema_from_path("graphql_server/schema/")
        schema = make_executable_schema(type_defs, query, mutation, user)

        self._server = CORSMiddleware(
                            GraphQL(schema, debug=debug),
                            allow_origins=["*"],
                            allow_headers=["*"],
                            allow_methods=["*"])

    def get_server(self) -> GraphQL:
        return self._server
