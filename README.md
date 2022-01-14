# Basic ETL with FastAPI

```yaml
Author: Mitch Murphy
Date: 2022-01-13
Description: ETL with FastAPI
```


## Introduction

## Getting Started

First run the manager: `uvicorn src.manage:create_app --factory --host 0.0.0.0 --port 8220`

Then run the first worker: `uvicorn --host 0.0.0.0 --port 8221 job_worker:server --workers=5`

_More to come..._