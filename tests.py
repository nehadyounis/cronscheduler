import unittest
from scheduler import Scheduler
from parsers import IntervalParser, CronSyntaxParser


class TestParsers(unittest.TestCase):

    def test_interval_parsers(self):
        self.assertAlmostEqual(IntervalParser.parse("30s"), 30)
        self.assertAlmostEqual(IntervalParser.parse("1h"), 3600)
        self.assertAlmostEqual(IntervalParser.parse("1h1s"), 3601)
        self.assertAlmostEqual(IntervalParser.parse("1h1m"), 3660)
        self.assertAlmostEqual(IntervalParser.parse("1d"), 86400)
        self.assertAlmostEqual(IntervalParser.parse("1s1h"), 3601)
        self.assertAlmostEqual(IntervalParser.parse(""), 0)

        with self.assertRaises(ValueError):
            IntervalParser.parse("1x")
        with self.assertRaises(ValueError):
            IntervalParser.parse("1 s")
        with self.assertRaises(ValueError):
            IntervalParser.parse("12m12c")
        with self.assertRaises(ValueError):
            IntervalParser.parse("1sx")
        with self.assertRaises(ValueError):
            IntervalParser.parse("1ss")
        with self.assertRaises(ValueError):
            IntervalParser.parse("1ssm")
        with self.assertRaises(ValueError):
            IntervalParser.parse("1")

    def test_cron_parser(self):
        self.assertAlmostEqual(CronSyntaxParser.parse("* * * * * * *"), [[], [], [], [], [], [], []])
        self.assertAlmostEqual(CronSyntaxParser.parse("0/15 * * ? 2 2,3 2020-2022"),
                               [[0, 15, 30, 45], [], [], [], [2], [2, 3], [2020, 2021, 2022]])
        self.assertAlmostEqual(CronSyntaxParser.parse("0 * * ? feb mon,tue 2020,2022"),
                               [[0], [], [], [], [2], [2, 3], [2020, 2022]])


def print_hi():
    print("hi")


class TestScheduler(unittest.TestCase):
    s = Scheduler()

    def setUp(self) -> None:
        self.s.kill_all()

    def test_job_assigning(self):
        with self.assertRaises(ValueError):
            self.s.add_job(print_hi, frequency=5, cron="* * * * * * *", identifier="stuff")
        with self.assertRaises(ValueError):
            self.s.add_job(print_hi, identifier="stuff")
        with self.assertRaises(ValueError):
            self.s.add_job(print_hi, frequency=5, )
        with self.assertRaises(ValueError):
            self.s.add_job(None, frequency=5, identifier="stuff")
