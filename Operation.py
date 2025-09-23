from datetime import timedelta
from Route import hours
from enum import Enum

class OprName(Enum):
    A = '0'
    B = '1'
    C = '2'
    D = '4'
    E = '5'
    F = '6'
    G = '7'
    H = '8'
    I = '9'
    J = '12'
    K = '58'
    L = '60'
    M = '61'
    N = '111'
    O = '300'
    P = '343'



class Operation:
    def __init__(self, id, time_start, time_end, employee, grade):
        self.id = id
        self.time = hours(time_end - time_start)
        self.time_start = time_start
        self.time_end = time_end
        self.employee = employee
        self.grade = grade
