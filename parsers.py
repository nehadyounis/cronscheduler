from typing import List


class IntervalParser:

    @staticmethod
    def parse(interval):
        # returns amount of seconds in a time interval string.
        if interval is None:
            return None
        seconds = 0
        collector = ""
        for letter in interval:
            if letter.isdigit():
                collector += letter
            else:
                num = int(collector)
                collector = ""

                if letter == 's':
                    seconds += num
                if letter == 'm':
                    seconds += num * 60
                if letter == 'h':
                    seconds += num * 3600
                if letter == 'd':
                    seconds += num * 86400
        return seconds


class CronSyntaxParser:

    @staticmethod
    def convert_cron_to_numeric(cron_str: str):
        months = "jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec"
        months = months.split(",")
        weekDays = "sat,sun,mon,tue,wed,thu,fri"
        weekDays = weekDays.split(",")
        cron_str = cron_str.lower()
        for i in range(len(months)):
            cron_str = cron_str.replace(months[i], f'{i + 1}')
        for i in range(len(weekDays)):
            cron_str = cron_str.replace(weekDays[i], f'{i}')
        return cron_str

    @staticmethod
    def parse(cron_string):
        if type(cron_string) != str:
            raise TypeError('Invalid cron string')
        cron_string = CronSyntaxParser.convert_cron_to_numeric(cron_string)
        parts = cron_string.strip().split()
        if len(parts) < 5:
            raise ValueError("Invalid cron string format")
        cron_parts = [[], [], [], [], [], [], []]
        for i in range(len(parts)):
            part = parts[i]

            if part == '*' or part == '?':
                continue
            elements = part.split(",")
            for elem in elements:
                if elem.find("-") == -1 and elem.find("/") == -1:
                    cron_parts[i].append(int(elem))
                if elem.find("-") != -1:
                    start = int(elem.split("-")[0])
                    end = int(elem.split("-")[1])
                    for j in range(start, end + 1):
                        cron_parts[i].append(j)
                if elem.find("/") != -1:
                    start = int(elem.split("/")[0])
                    interval = int(elem.split("/")[1])
                    end = 59
                    if i == 2: end = 23
                    if i == 3: end = 31
                    if i == 4: end = 12
                    if i == 5: end = 6
                    while start < end:
                        cron_parts[i].append(start)
                        start += interval

                    for j in range(start, end + 1):
                        cron_parts[i].append(j)

        return cron_parts
