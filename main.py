import time
from datetime import datetime
from scheduler import Scheduler
from job import Job

from parsers import IntervalParser, CronSyntaxParser

def print_hi():
    now = datetime.now()
    time.sleep(3)
    print(f'Hi, {now}')

def print_no():
    now = datetime.now()
    time.sleep(3)
    print(f'No, {now}')
    return "yup"

def print_eww():
    now = datetime.now()
    print(f'Eww, {now}')


if __name__ == '__main__':
    pass
    # j = Job(print_hi,"ayoo", 0, 1644605650)
    # j.print_info()
    s = Scheduler()
    s.add_job(print_no, identifier="no", frequency='10s', max_times=5)
    # s.add_job(print_no, identifier="no", frequency=3, max_times=5)
    # s.add_job(print_eww, identifier="eww", frequency=1, max_times=10)
    s.add_job(print_hi, identifier="hi", cron="0/10 * * ? 2 * 2020-2025")
    s.run()
    #print(CronSyntaxParser.parse("0/10 10,44 14 ? 3 WED 2002-2005"))




