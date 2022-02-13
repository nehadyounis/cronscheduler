class IntervalParser:

    @staticmethod
    def parse(interval: str):
        """
        This function receives a string of time interval and returns the corresponding values in seconds

        :param interval: (str) an interval string, ex. "1m30s"
        :return: (int) the corresponding value of that interval in seconds, ex. 90

        e.g "30m" --> returns 1800
        e.g "20s" --> returns 20
        e.g "1m30s" --> returns 90
        e.g "1h" --> returns 3600
        e.g "1d" --> returns 86400

        accepted letters are:
        s -> seconds
        m -> minutes
        h -> hours
        d -> days
        any other letters and the numbers previous to them will be ignored.
        """

        if interval is None:
            return 0
        if interval.find(" ") != -1:
            raise ValueError("Interval cannot contain spaces")
        seconds = 0
        collector = "0"  # a string to collect each part of the interval.
        for letter in interval:
            if letter.isdigit():
                collector += letter
            else:
                num = int(collector)
                collector = "0"

                if letter == 's':  # seconds
                    seconds += num
                if letter == 'm':  # minutes
                    seconds += num * 60
                if letter == 'h':  # hours
                    seconds += num * 3600
                if letter == 'd':  # days
                    seconds += num * 86400
        return seconds


class CronSyntaxParser:

    @staticmethod
    def convert_cron_to_numeric(cron_str: str):
        """
        converts cron syntax that has letters (ex. wed, fri, apr) to numeric cron syntax
        e.g. 0/5 * * ? feb mon,tue 2020-2025 --> 0/5 * * ? 2 1,2 2020-2025
        :param cron_str: (str) a cron string that might contain letters
        :return: (str) a cron string with no letters
        """
        months = "jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec"
        months = months.split(",")
        weekDays = "sat,sun,mon,tue,wed,thu,fri"
        weekDays = weekDays.split(",")
        cron_str = cron_str.lower()
        for i in range(len(months)):
            cron_str = cron_str.replace(months[i], f'{i + 1}')  # replacing every month name with corresponding number
        for i in range(len(weekDays)):
            cron_str = cron_str.replace(weekDays[i], f'{i}')    # replacing every weekday name with corresponding number
        return cron_str

    @staticmethod
    def parse(cron_string) -> list:
        """
        This function receives a string of cron syntax and returns a list of lists, corresponding to all the
        days, months ... etc. at which the job shall be executed

        :param cron_string: (str) a cron syntax string
        :return: list[7][]: A list of corresponding days, minutes ... etc. at which the job shall be executed

        e.g.
        string = 0/15 * * ? feb 2,3 2020-2022
        returned list = [[0,15,30,45], [], [], [], [2], [2, 3], [2020, 2021, 2022]]

        empty list means all values are allowedx
        """

        if type(cron_string) != str:
            raise TypeError('Invalid cron string')

        cron_string = CronSyntaxParser.convert_cron_to_numeric(cron_string)
        parts = cron_string.strip().split()
        if len(parts) < 5:
            raise ValueError("Invalid cron string format")
        cron_parts = [[], [], [], [], [], [], []]
        for i in range(len(parts)):
            part = parts[i]

            if part == '*' or part == '?':  # all values are allowed
                continue
            elements = part.split(",")  # parsing multiple values, e.g. 23,24-26, 0/20 to list = [23, 24-26, 0/5]
            for elem in elements:
                if elem.find("-") == -1 and elem.find("/") == -1:  # a single entity e.g 23
                    cron_parts[i].append(int(elem))

                if elem.find("-") != -1:    # a range, e.g. 24-26 -> 24, 25, 26
                    start = int(elem.split("-")[0])
                    end = int(elem.split("-")[1])
                    for j in range(start, end + 1):
                        cron_parts[i].append(j)

                if elem.find("/") != -1:   # a multiplier, e.g. 0/20 -> 0, 20, 40
                    start = int(elem.split("/")[0])
                    interval = int(elem.split("/")[1])

                    if i == 2: end = 23
                    elif i == 3: end = 31
                    elif i == 4: end = 12
                    elif i == 5: end = 6
                    else: end = 59

                    while start < end:
                        cron_parts[i].append(start)
                        start += interval

        return cron_parts
