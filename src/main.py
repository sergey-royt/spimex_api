from fastapi import FastAPI


def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    return fastapi_app


app = create_app()
