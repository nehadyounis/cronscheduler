import time
from datetime import datetime
from scheduler import Scheduler
import mock

from parsers import IntervalParser, CronSyntaxParser


def print_hi():
    time.sleep(2)  # hypothitical execution time
    print(f'Hi')
    return "I said hi"


def print_no():
    now = datetime.now()
    time.sleep(3)
    print(f'No, {now}')
    return "yup"


def print_eww():
    now = datetime.now()
    print(f'Eww, {now}')



if __name__ == '__main__':
    # j = Job(print_hi,"ayoo", 0, 1644605650)
    # j.print_info()
    s = Scheduler()
    # s.add_job(print_hi, identifier="job_hi", frequency='5s', max_times=5, expected_time="1s")
    # s.add_job(print_no, identifier="no", frequency=3, max_times=5)
    # s.add_job(print_eww, identifier="eww", frequency=1, max_times=10)
    s.add_job(print_hi, identifier="hi", cron="0/5 * * ? 2 * 2020-2025")
    #   s  m  h dof m dow y
    print(s.num_of_jobs())
    print(s.jobs_ids())

    # print(CronSyntaxParser.parse("0/10 10,44 14 ? 3 WED 2002-2005"))

# 0 0-30 12-13 * * * *"
