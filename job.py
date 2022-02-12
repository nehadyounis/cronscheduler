import datetime
import time
from parsers import IntervalParser, CronSyntaxParser
import logging

logging.basicConfig(filename="intervals.log",
                    level=logging.INFO,
                    format='%(asctime)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')


class Job:
    cronSyntax: str = None
    func = None
    identifier: str = None
    expectedExecutionTime: int = None
    actualExecutionTime: int = None
    frequency: int = None
    maxTimes: int = None
    timesLeft: int = None
    lastRunTimeStamp: int = None
    nextRunTimeStamp: int = None
    delay: int = None
    cronList = []

    __ret = None

    def __init__(self, func, cron=None, identifier=None, frequency=None, delay=0, expected_time=None, max_times=None):
        self.func = func
        self.identifier = identifier
        self.expectedExecutionTime = expected_time
        self.frequency = frequency
        self.delay = delay
        self.maxTimes = max_times
        self.cronSyntax = cron

        self.timesLeft = max_times

        if self.frequency is not None:
            self.nextRunTimeStamp = int(time.time()) + frequency
        else:
            self.cronList = CronSyntaxParser.parse(cron)

    def print_info(self):

        print(f"Identifier: {self.identifier}")
        print(f"expectedExecutionTime: {self.expectedExecutionTime}")
        print(f"actualExecutionTime: {self.actualExecutionTime}")
        print(f"frequency: {self.frequency}")
        print(f"cronSyntax: {self.cronSyntax}")

    def execute(self):
        if self.timesLeft is not None:
            self.timesLeft -= 1
        self.lastRunTimeStamp = int(time.time())
        if self.frequency is not None:
            self.nextRunTimeStamp = self.lastRunTimeStamp + self.frequency
        start = time.time()
        self.__ret = self.func()
        end = time.time()
        self.actualExecutionTime = end - start

        logging.info(self.log_string())

    def log_string(self):
        log_string = f"id:{self.identifier}, expected time:{self.expectedExecutionTime}, actual time: {round(self.actualExecutionTime)}s"
        if self.__ret is not None:
            log_string += f", return: {self.__ret}"
        return log_string

    def timeToRun(self):
        if self.frequency is not None:
            return self.nextRunTimeStamp == int(time.time()) and self.timesLeft != 0
        else:
            dt = datetime.datetime.now()
            tests = [False] * 7
            tests[0] = len(self.cronList[0]) == 0 or dt.second in self.cronList[0]
            tests[1] = len(self.cronList[1]) == 0 or dt.minute in self.cronList[1]
            tests[2] = len(self.cronList[2]) == 0 or dt.hour in self.cronList[2]
            tests[3] = len(self.cronList[3]) == 0 or dt.day in self.cronList[3]
            tests[4] = len(self.cronList[4]) == 0 or dt.month in self.cronList[4]
            tests[5] = len(self.cronList[5]) == 0 or dt.weekday() + 1 in self.cronList[5]
            tests[6] = len(self.cronList[6]) == 0 or dt.year in self.cronList[6]

            return all(tests)
