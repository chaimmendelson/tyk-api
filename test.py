# import strawberry
# from horizon_fastapi_template import general_create_app
# from horizon_fastapi_template.utils import GraphQLVersion

# @strawberry.type
# class Query:
#     @strawberry.field
#     def hello(self) -> str:
#         return "world"

# schema = strawberry.Schema(query=Query)

# graphql_versions = [GraphQLVersion(
#     version="v1",
#     graphql_schema=schema,
# )]

# app = general_create_app(
#     graphql_versions=graphql_versions
# )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # To test the GraphQL endpoint, you can run this script and then navigate to
# # http://localhost:8000/graphql/v1/playground in your web browser. 
# # You should see the GraphQL Playground where you can execute the following query:
# # {
# #   hello
# # }
# # The expected response should be:
# # {
# #   "data": {
# #     "hello": "world"
# #   }
# # }

import jwt

token = jwt.encode(
    {
        "iss": "portswigger",
        "exp": 1782286676,
        "sub": "administrator"
    },
    "hello",
    algorithm="HS256"
)

print(token)