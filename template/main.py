from contextlib import asynccontextmanager
from os import getenv

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import create_type

# database imports
from .db import ensure_samples_index

# override PyObjectId and Context scalars
from .models import PyObjectId
from .otypes import Context, PyObjectIdType

# import all queries and mutations
from .queries import queries
from .mutations import mutations


# create query types
Query = create_type("Query", queries)

# create mutation types
Mutation = create_type("Mutation", mutations)


# override context getter
async def get_context() -> Context:
    return Context()


# initialize federated schema
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    enable_federation_2=True,
    scalar_overrides={PyObjectId: PyObjectIdType},
)

# Get env variable of whether to run application in Debug Mode
DEBUG = getenv("TEMPLATE_DEBUG", "false").lower() in ("true", "1", "t")

# Make GraphQL Router
gql_app = GraphQLRouter(schema, graphiql=True, context_getter=get_context)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await ensure_samples_index()
    yield
    # Shutdown

# serve API with FastAPI router
app = FastAPI(
    debug=DEBUG,
    title="BB Template",
    desciption="Integration of FastAPI, Strawberry and Pydantic with Mondodb using pymongo",
    port=5000,
)
app.include_router(gql_app, prefix="/graphql")

# Add backend running confirmation
@app.get("/")
async def ping():
    return {"ping": "pong"}