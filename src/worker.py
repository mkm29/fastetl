import asyncio, os
from fastapi import FastAPI
from easyjobs.workers.worker import EasyJobsWorker

from .secrets import SECRET_KEY

server = FastAPI()


@server.on_event("startup")
async def setup():
    worker = await EasyJobsWorker.create(
        server,
        server_secret=SECRET_KEY,
        manager_host="0.0.0.0",
        manager_port=8220,
        manager_secret=SECRET_KEY,
        jobs_queue="ETL",
        max_tasks_per_worker=5,
    )

    every_minute = "* * * * *"
    default_args = {"args": ["http://stats"]}

    async def get_data(url):
        return {"a": 1, "b": 2, "c": 3}

    async def load_db(data: dict):
        # await db.tables['transformed'].insert(**data)
        await asyncio.sleep(5)
        return f"data {data} loaded to db"

    async def send_email(address: str, message: str):
        return f"email sent to {address}"

    @worker.task(
        run_after=["transform"], schedule=every_minute, default_args=default_args
    )
    async def extract(url: str):
        print(f"extract started")
        data = await get_data(url)
        return {"data": data}

    @worker.task(run_after=["load"])
    async def transform(data: dict):
        print(f"transform started")
        for k in data.copy():
            data[k] = int(data[k]) + 2
        return {"data": data}

    @worker.task(on_failure="failure_notify", run_after=["compute"])
    async def load(data):
        print(f"load started")
        await load_db(data)
        return {"data": data}

    @worker.task()
    async def failure_notify(job_failed):
        await send_email("admin@company.io", job_failed)
        return job_failed

    @worker.task()
    async def deploy_environment():
        print(f"deploy_environment - started")
        await asyncio.sleep(5)
        print(f"deploy_environment - completed")
        return f"deploy_environment - completed"

    @worker.task()
    async def prepare_db():
        print(f"prepare_db - started")
        await asyncio.sleep(5)
        print(f"prepare_db - completed")
        return f"deploy_environment - completed"

    @worker.task(run_before=["deploy_environment", "prepare_db"])
    async def configure_environment():
        print(f"pre_compute - starting")
        await asyncio.sleep(5)
        print(f"pre_compute - finished")
        return f"pre_compute - finished"

    os.environ["WORKER_TASK_DIR"] = "/home/codemation/subprocesses"

    @worker.task(subprocess=True, run_before=["configure_environment"])
    async def compute(data: dict):
        pass
