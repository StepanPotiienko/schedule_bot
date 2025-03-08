import datetime


class Date:
    def __init__(self, dateObject: datetime):
        self.dateObject = dateObject

    def get_day(self):
        return self.dateObject.day

    def get_month(self):
        return self.dateObject.month

    def get_year(self):
        return self.dateObject.year
