from datetime import timedelta
from Route import hours

class Operation:
    def __init__(self, name, time_start, time_end, employee, grade):
        self.name = name
        self.time = hours(time_end - time_start)
        self.time_start = time_start
        self.time_end = time_end
        self.employee = employee
        self.grade = grade
