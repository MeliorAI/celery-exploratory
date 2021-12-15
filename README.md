# Celery Exploratory

This repo demostrate how to build a very basic Celery distributed task system.

<!--ts-->
   * [Celery Exploratory](#celery-exploratory)
      * [Install](#install)
      * [How To](#how-to)

<!-- Added by: jose, at: Wed Dec 15 16:32:40 UTC 2021 -->

<!--te-->

## Install

```bash
pip install -r requirements.txt
```

## How To

1. Run `rabbitMQ` and `redis` as Celery backends

    ```bash
    docker-compose up
    ```

2. Run the app (server):

    ```bash
    celery -A src worker -l INFO
    ```

3. Call the functions

    * To test an individuall function:

    ```python
    from src.tasks import add

    add.delay(2, 2).get(timeout=1)
    ```


    Or to run the client: `make run-client f=<file-to-extract-text-from>`

