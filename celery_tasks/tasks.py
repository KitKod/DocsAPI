import sys
sys.path.append('..')

import datetime

from celery import Celery

from api.database_controller import DocsTableManipulator


celery_app = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq:5672/')


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(20.0, make_report.s(), name='add every 50')


@celery_app.task
def make_report():
    docs_table = DocsTableManipulator()
    now = datetime.date.today()
    result = len(docs_table.get_doc_by_date(now))

    with open('/usr/src/app/reports/report.txt', 'a') as f:
        if result:
            f.write('<{}> - {}\n'.format(now, result))
