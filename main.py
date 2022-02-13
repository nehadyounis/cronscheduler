import time
from scheduler import Scheduler



def print_hi():
    time.sleep(2)  # hypothetical execution time
    print(f'Hi')
    return "I said hi"


if __name__ == '__main__':
    s = Scheduler()
    s.add_job(print_hi, identifier="job_hi", frequency='10s', max_times=5)
    s.add_job(print_hi, identifier="hi", cron="0/5 * * ? 2 * 2020-2025")
    print(s.num_of_jobs())
    print(s.jobs_ids())
    s.run()


# 0 0-30 12-13 * * * *"
