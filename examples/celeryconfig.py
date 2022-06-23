broker_url = 'redis://127.0.0.1:6379/0'
# broker_url = 'pyamqp://localhost:5672'
celery_result_backend = 'redis://127.0.0.1:6379/1'
task_send_sent_event = False
