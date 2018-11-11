from __future__ import absolute_import

from datetime import timedelta

from celery.task import periodic_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@periodic_task(run_every=timedelta(seconds=30))
def crawl_domain():
    print("crawl_task")
    from .crawl import domain_crawl
    return domain_crawl()