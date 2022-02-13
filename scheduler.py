from job import Job
from typing import List, Callable
from threading import Thread
from parsers import IntervalParser
import time


class Scheduler(object):
    """
    # Telda Coding Challenge: Cron scheduler
This is my attempt to solve telda's coding challenge, which is to Implement an in-process cron scheduler that accepts a
job and executes it periodically.

## Requirements
Clients should be able to specify:

- A single run expected interval, e.g. `30m`.
- Scheduling frequency, e.g. `1hr` for a job that should run every one hour.
- The job implementation, e.g. a function.
- A unique job identifier.

## Solution
This is a python package that can schedule tasks and execute them in parallel on specefici times, as well as logging all
the jobs that have been done.

### Usage
To use this package, import it to any project
```python
from scheduler import Scheduler
```

Then initialize a scheduler, add jobs to it and put it to run, that's it.

```python
def print_hi():
    print('Hi')

s = Scheduler()
s.add_job(print_hi, identifier="job_hi", frequency='10s', max_times=5)
s.run()
```


You can set jobs intervals using two methods, the first is determining a frequency for the job using `frequency` attribute

```python
s.add_job(print_hi, identifier="job_hi1", frequency='10s') #Executes every 10 seconds, infinite number of times
s.add_job(print_hi, identifier="job_hi2", frequency='10s', max_times=5) #Executes every 10 seconds for 5 times.
s.add_job(print_hi, identifier="job_hi3", frequency='1m', max_times=5) #Executes every 1 minute for 5 times.
s.add_job(print_hi, identifier="job_hi4", frequency='3h3m10s') #Executes every 3 hours 30 minute 10 seconds, infinite number of times
s.add_job(print_hi, identifier="job_hi5", frequency='1d', max_times=5) #Executes every day for 5 times.
```

Or you can use Cron Syntax to specifiy when the job shall be executed

```python
s.add_job(print_hi, identifier="hi1", cron="0 0 12 * * ?") #Fire at 12:00 PM (noon) every day
s.add_job(print_hi, identifier="hi2", cron="0 10,44 14 ? 3 WED") #Fire at 2:10 PM and at 2:44 PM every Wednesday in the month of March
s.add_job(print_hi, identifier="hi3", cron="0 0 12 1/5 * 2022,2023") #Fire at 12 PM (noon) every 5 days every month, starting on the first day of the month, years 2022 and 2023
s.add_job(print_hi, identifier="hi4", cron="0 15 10 ? * MON-FRI") #Fire at 10:15 AM every Monday, Tuesday, Wednesday, Thursday and Friday
```

Expected execution time can be added as an optional argument
```python
s.add_job(print_hi, identifier="job_hi1", frequency='10s', expected_time='1s')
```
Logging can be found in the file intervals.log, for exapmle, this code produces that following log

```python
def print_hi():
    time.sleep(2) # hypothitical execution time
    print(f'Hi')
    return "I said hi"

if __name__ == '__main__':
    s = Scheduler()
    s.add_job(print_hi, identifier="job_hi", frequency='5s', max_times=5, expected_time="1s")
    s.run()
```

```log
02/12/2022 05:30:30: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:35: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:40: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:45: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
02/12/2022 05:30:50: id:job_hi, expected time:1s, actual time: 2s, return: I said hi
```

    """

    running = False

    def __init__(self) -> None:
        self.jobs: List[Job] = []

    def add_job_object(self, job: Job):
        """
        Adds a job object to the scheduler, it doesn't check the validity of the job

        :param job: (Job)
        :return: None
        """
        self.jobs.append(job)

    def add_job(self, func: Callable, cron=None, identifier=None, frequency=None, expected_time="0s", max_times=None):
        """
        Add a Job to the scheduler

        :param func: (Callable) a function to be repeated by the scheduler, cannot be None
        :param cron: (str) a cron syntax to specify job execution intervals, e.g "0 30 0 ? * wed 2022"
        :param identifier: (str) a string to uniquely identify a job, cannot be None
        :param frequency: (str) an interval string to specify job execution intervals, e.g "1h30m"
        :param expected_time: (str) an interval string for the expected execution time.
        :param max_times:  (int) how many times do you want this job to be executed, leave blank if infinity
        :return: None
        """

        if cron and frequency:
            raise ValueError("Cron syntax and frequency cannot be assigned together")
        if not cron and not frequency:
            raise ValueError("Either cron syntax or frequency must have a value")
        if not func:
            raise ValueError("Function to be executed cannot be None")
        if not identifier or identifier == "":
            raise ValueError("Identifier cannot be None or blank")
        for job in self.jobs:
            if job.identifier == identifier:
                raise ValueError("A job with this identifier already exists")

        frequencyInSeconds = None
        if frequency:
            frequencyInSeconds = IntervalParser.parse(frequency)
        expectedTimeInSeconds = IntervalParser.parse(expected_time)

        currentJob: Job = Job(func, cron, identifier, frequencyInSeconds, expectedTimeInSeconds, max_times)
        self.jobs.append(currentJob)

    def kill_all(self):
        """
        deletes all the jobs in the current schedule

        :return:
        """
        self.stop()
        self.jobs.clear()

    def kill_job(self, identifier: str):
        """
        deletes a specific job using its identifier

        :param identifier: (str) job identifier
        :return:
        """
        self.jobs = list(filter(lambda x: x.identifier != identifier, self.jobs))

    def jobs_ids(self):
        """
        returns a list of job identifiers currently on schedule

        :return: (list) a list of strings
        """
        identifiersList = []
        for job in self.jobs:
            identifiersList.append(job.identifier)
        return identifiersList

    def num_of_jobs(self):
        """
        returns number of jobs on the schedule

        :return: (int)
        """
        return len(self.jobs)

    def __run_on_thread(self):
        self.running = True
        while self.running:
            for job in self.jobs:
                if job.time_to_run():
                    thread = Thread(target=job.execute)
                    thread.run()
            time.sleep(1)

    def run(self):
        """
        Run the schedule on an independent thread, this function won't stop any other tasks from being executed

        :return: None
        """
        if not self.running:
            main_thread = Thread(target=self.__run_on_thread)
            main_thread.start()
        else:
            print("Schedule is already running")

    def stop(self):
        """
        Stops the current schedule

        :return: None
        """
        self.running = False
