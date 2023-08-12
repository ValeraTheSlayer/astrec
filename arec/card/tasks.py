from celery import shared_task


@shared_task
def long_running_task():
    # Здесь выполняется длительная операция
    pass
