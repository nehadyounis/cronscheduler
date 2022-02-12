from job import Job
from typing import List
from threading import Thread
import time
from parsers import IntervalParser, CronSyntaxParser


class Scheduler(object):
    running = False

    def __init__(self) -> None:
        self.jobs: List[Job] = []

    def add_job_object(self, job: Job):
        self.jobs.append(job)

    def add_job(self, func, cron=None, identifier=None, frequency=None, delay=0, expected_time="0s", max_times=None):
        if (cron is not None) and (frequency is not None):
            raise AttributeError("Cron syntax and frequency cannot be assigned together")
        if (cron is None) and (frequency is None):
            raise AttributeError("either cron syntax or frequency must have a value")
        if func is None:
            raise AttributeError("Function to be executed cannot be None")
        for job in self.jobs:
            if job.identifier == identifier:
                raise AttributeError("A job with this identifier already exists")

        frequencyInSeconds = None
        if frequency is not None:
            frequencyInSeconds = IntervalParser.parse(frequency)
        expectedTimeInSeconds = IntervalParser.parse(expected_time)

        j: Job = Job(func, cron, identifier, frequencyInSeconds, delay, expected_time, max_times)
        self.jobs.append(j)

    def __run_on_thread(self):
        self.running = True
        while self.running:
            for job in self.jobs:
                if job.timeToRun():
                    thread = Thread(target=job.execute)
                    thread.run()
            time.sleep(1)

    def run(self):
        x = Thread(target=self.__run_on_thread)
        x.start()

    def stop(self):
        self.running = False
