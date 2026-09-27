from horizon_fastapi_template import general_create_app
from horizon_fastapi_template.utils import GraphQLVersion
from .src import add_routers

from tyk_api.src.graphql import schema as graphql_schema


# Create app with GraphQL enabled (schema v1)
app = general_create_app(graphql_versions=[GraphQLVersion(graphql_schema=graphql_schema.schema)])

add_routers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)