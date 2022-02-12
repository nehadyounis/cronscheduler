import unittest
import time
from datetime import datetime
from scheduler import Scheduler
from parsers import IntervalParser, CronSyntaxParser
from job import Job
import functools
import mock


class TestParsers(unittest.TestCase):

    def test_interval_parsers(self):
        self.assertAlmostEqual(IntervalParser.parse("30s"),30)
        self.assertAlmostEqual(IntervalParser.parse("30ss"), 30)
        self.assertAlmostEqual(IntervalParser.parse("30ssm"), 30)
        self.assertAlmostEqual(IntervalParser.parse("1h"), 3600)
        self.assertAlmostEqual(IntervalParser.parse("1h1s"), 3601)
        self.assertAlmostEqual(IntervalParser.parse("1h1m"), 3660)
        self.assertAlmostEqual(IntervalParser.parse("1d"), 86400)
        self.assertAlmostEqual(IntervalParser.parse("1s1h"), 3601)
        self.assertAlmostEqual(IntervalParser.parse("1dddddd"), 86400)
        self.assertAlmostEqual(IntervalParser.parse("1x"), 0)
        self.assertAlmostEqual(IntervalParser.parse(""), 0)

    def test_cron_parser(self):
        self.assertAlmostEqual(CronSyntaxParser.parse("* * * * * * *"), [[], [], [], [], [], [], []])
        self.assertAlmostEqual(CronSyntaxParser.parse("0/15 * * ? 2 2,3 2020-2022"), [[0,15,30,45], [], [], [], [2], [2, 3], [2020, 2021, 2022]])
        self.assertAlmostEqual(CronSyntaxParser.parse("0 * * ? feb mon,tue 2020,2022"), [[0], [], [], [], [2], [2, 3], [2020, 2022]])



class TestScheduler(unittest.TestCase):
    s = Scheduler()

    def setUp(self) -> None:
        self.s.kill_all()

    def test_job_assigning(self):
        pass
