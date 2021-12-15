# Celery Exploratory

This repo demostrate how to build a very basic Celery distributed task system.

<!--ts-->
   * [Celery Exploratory](#celery-exploratory)
      * [Requirements](#requirements)
      * [How To](#how-to)
         * [Install](#install)
         * [Run](#run)

<!-- Added by: jose, at: Wed Dec 15 16:43:55 UTC 2021 -->

<!--te-->

## Requirements

 - python >= 3.6
 - docker
 - docker-compose

## How To

### Install

Installing should be as simple as:

```bash
make insall
```

Assuming `docker` and `docker-compose` are already installed in your system


### Run

1. Run `rabbitMQ` and `redis` as Celery backends

    ```bash
    docker-compose up
    ```

2. Run the app (server):

    ```bash
    make run-workers
    ```

3. Call the functions

    * To test an individuall function:

        ```python
        from src.tasks import add

        add.delay(2, 2).get(timeout=1)
        ```

    * Or to run text-extraction functions from the client:

        ```bash
        make run-client f=<file-to-extract-text-from>
        ```
