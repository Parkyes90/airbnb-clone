import calendar
import datetime
import time


class Day:
    def __init__(self, number, past):
        self.number = number
        self.past = past

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                if day != 0:
                    now = time.time()
                    u_time = time.mktime(
                        datetime.datetime.strptime(
                            f"{self.year}{self.month}{day}", "%Y%m%d"
                        ).timetuple()
                    )
                    new_day = Day(day, now >= u_time)
                else:
                    new_day = Day(day, False)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]
