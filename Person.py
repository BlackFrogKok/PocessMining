from datetime import timedelta
from datetime import datetime as dt

# fromisoformat()

class Person:
    def __init__(self, route_names, time_start, time_end, opr_time, opr_start_date,
                 chanel, type_strah, damage, place, summ, grade):
        self.route_names: list = route_names
        self.time_start = time_start
        self.time_vipol = (time_end - time_start)
        self.opr_time = opr_time
        self.opr_start_date = opr_start_date
        self.chanel = chanel
        self.type_strah = type_strah
        self.damage = damage
        self.place = place
        self.summ = summ
        self.grade = grade

    def is_over_limit(self):
        return self.time_vipol >= timedelta(days=2)

