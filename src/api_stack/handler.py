import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from api import ExampleApi

example_api = ExampleApi(os.environ['table'])
app = FastAPI(openapi_prefix="/prod/") # Replace with your STG environment in API Gateway
app.include_router(example_api.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Modify for whitelisting
    allow_credentials=True,
    allow_methods=["*"], # Adjust for your use case
    allow_headers=["*"] # Also adjust for your use case
)

def lambda_handler(event, context):
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
