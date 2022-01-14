""" Main primary ETL module """

import asyncio, os
from easyjobs.manager import EasyJobsManager
from fastapi import FastAPI

def create_app() -> FastAPI:
    """ Factory method for creating FastAPI app. """
    app = FastAPI()

    @app.on_event('startup')
    async def startup():
        app.job_manager = await EasyJobsManager.create(
            app,
            server_secret='6a0d9933d3ad40b882ad84c7'
        )

    return app