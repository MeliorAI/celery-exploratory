# Celery 101

This repo demostrate how to build a very basic Celery distributed task system.

## Install

```bash
pip install -r requirements.txt
```

## How To

1. Run `rabbitMQ`

    ```bash
    ./run_rabbit.sh
    ```

2. Run the app (server):

    ```bash
    celery -A src worker -l INFO
    ```

3. Call the functions

    ```python
    from src.tasks import add

    add.delay(2, 2).get(timeout=1)

    ```
    You could also do : python -m src.main "path" to test how textract functions are executed remotely with celery .
