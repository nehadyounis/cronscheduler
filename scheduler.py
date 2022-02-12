from job import Job
from typing import List
from threading import Thread
import time
from parsers import IntervalParser


class Scheduler(object):
    running = False

    def __init__(self) -> None:
        self.jobs: List[Job] = []

    def add_job_object(self, job: Job):
        self.jobs.append(job)

    def add_job(self, func, cron=None, identifier=None, frequency=None, delay=0, expected_time="0s", max_times=None):
        if (cron is not None) and (frequency is not None):
            raise ValueError("Cron syntax and frequency cannot be assigned together")
        if (cron is None) and (frequency is None):
            raise ValueError("either cron syntax or frequency must have a value")
        if func is None:
            raise ValueError("Function to be executed cannot be None")
        if identifier is None or identifier == "":
            raise ValueError("Identifier cannot be None or blank")
        for job in self.jobs:
            if job.identifier == identifier:
                raise ValueError("A job with this identifier already exists")

        frequencyInSeconds = None
        if frequency is not None:
            frequencyInSeconds = IntervalParser.parse(frequency)
        expectedTimeInSeconds = IntervalParser.parse(expected_time)

        j: Job = Job(func, cron, identifier, frequencyInSeconds, delay, expected_time, max_times)
        self.jobs.append(j)

    def kill_all(self):
        self.stop()
        self.jobs.clear()

    def kill_job(self, identifier: str):
        self.jobs = list(filter(lambda x: x.identifier != identifier, self.jobs))

    def jobs_ids(self):
        identifiersList = []
        for job in self.jobs:
            identifiersList.append(job.identifier)
        return identifiersList

    def num_of_jobs(self):
        return len(self.jobs)

    def __run_on_thread(self):
        self.running = True
        while self.running:
            for job in self.jobs:
                if job.timeToRun():
                    thread = Thread(target=job.execute)
                    thread.run()
            time.sleep(1)

    def run(self):
        if not self.running:
            main_thread = Thread(target=self.__run_on_thread)
            main_thread.start()
        else:
            print("Schedule is already running")

    def stop(self):
        self.running = False
