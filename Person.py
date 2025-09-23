from datetime import timedelta
from enum import Enum
from datetime import datetime as dt

# fromisoformat()


class Person:
    def __init__(self, time_start, time_end, operations,
                 chanel, type_strah, damage, place, summ, grade):
        self.time_start = time_start
        self.time_vipol = (time_end - time_start)
        self.operations = operations

        self.chanel = chanel
        self.type_strah = type_strah
        self.damage = damage
        self.place = place
        self.summ = summ
        self.grade = grade

    def is_over_limit(self):
        return self.time_vipol >= timedelta(days=2)

