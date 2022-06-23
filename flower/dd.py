# -*- coding:utf-8 -*-
from celery import Celery


def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    def announce_success_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK SUCCEEDED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-succeeded': announce_success_tasks,
                '*': state.event,
        })
        print('*' * 10)
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    app = Celery(broker='redis://127.0.0.1:6379/0')
    my_monitor(app)
