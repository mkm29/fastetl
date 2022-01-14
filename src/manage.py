""" Manager module """

import asyncio, os
from easyjobs.manager import EasyJobsManager
from easyjobs.workers.worker import EasyJobsWorker
from fastapi import FastAPI

from .secrets import SECRET_KEY


def create_app() -> FastAPI:
    """ Factory method for creating FastAPI app. """
    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        app.job_manager = await EasyJobsManager.create(app, server_secret=SECRET_KEY)

    return app
