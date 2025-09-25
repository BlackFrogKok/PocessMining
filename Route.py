from datetime import timedelta
from statistics import median
import pandas as pd
import plotly.express as px


def sec(dt):
    return [i.total_seconds() / 3600 for i in dt]

def hours(dt):
    return dt.total_seconds() / 3600

def _render_opr_and_compl_time(persons, obedinenie):
    buffer = {}
    time_vipols_list = []
    proebishi = 0
    for person in persons:
        time_vipols_list.append(hours(person.time_vipol))
        if person.is_over_limit():
            proebishi += 1
        for id, opr in person.operations.items():
            if id in buffer:
                buffer[id] += opr.time
            else:
                buffer[id] = opr.time
    if obedinenie:
        obedinenie = obedinenie.split('+')
        buffer[obedinenie] = []
        for i in range(len(buffer[obedinenie[0]])):
            buffer[obedinenie].append(sum(buffer[j][i] for j in obedinenie))
    return buffer, time_vipols_list, proebishi



class Route:
    def __init__(self, route, persons, func=lambda x: x, obedinenie=None):
        self.route = route
        self.persons = list(filter(func, persons))

        self.opr_time, time_vipols_list, self.proebishi = _render_opr_and_compl_time(self.persons, obedinenie)
        self.avr_compl = sum(time_vipols_list) / len(time_vipols_list)
        self.mediana_vipol = median(time_vipols_list)
        self.avr_opr, self.mediana_opr = self._render_avr_mediana_opr()
        self.fraction = {k:(v / sum(self.avr_opr.values())) for k, v in self.avr_opr.items()}
        self.max_fraction_opr = max(self.fraction, key=self.fraction.get)
        self.dev_opr = self._render_deviation()
        
    def _render_avr_mediana_opr(self):
        avr_opr = {}
        mediana_opr = {}
        for opr, times in self.opr_time.items():
            avr_opr[opr] = sum(times) / len(times)
            mediana_opr[opr] = median(times)
        return avr_opr, mediana_opr

    def is_proverka(self):
        i = max(self.fraction, key=self.fraction.get)
        return i, (self.avr_opr[i]) / (self.mediana_opr[i])

    def _render_deviation(self):
        opr_dev = {}
        for opr, time in self.opr_time.items():
            opr_dev[opr] = [i - self.avr_opr[opr] for i in time]
        return opr_dev


    def get_operations(self, opr='all'):
        all_oprs = {}
        for sl in [i.operations for i in self.persons]:
            for k, v in sl.items():
                if opr == 'all' or k == opr:
                    if k in all_oprs:
                        all_oprs[k].append(v)
                    else:
                        all_oprs[k] = [v]
        return all_oprs


    def sample_persons_by_month(self):
        groups = {}
        for person in self.persons:
            if person.time_start.month > 9:
                time = str(person.time_start.year) + '.' + str(person.time_start.month)
            else:
                time = str(person.time_start.year) + '.0' + str(person.time_start.month)

            if time in groups:
                groups[time].append(person)
            else:
                groups[time] = [person]
        return groups

    def calc_cycle_ineff_time_route(self, opers_to_calc):
        inefficiency_by_month = {}
        groups = self.sample_persons_by_month()
        for time, persons in groups.items():
            inefficiency = 0
            for person in persons:
                inefficiency += person.clac_cycle_ineff_time_person(opers_to_calc)
            inefficiency_by_month[time] = inefficiency
        return inefficiency_by_month


    def hist_opr_time(self, opr, write=False):
        df = pd.DataFrame(dict(
            hours=[i.time for i in self.get_operations(opr=opr)[opr]]
        ))

        fig = px.histogram(df, x='hours', nbins=40, title=f'Время операции {opr} непостоянно')
        fig.show()
        if write:
            fig.write_image(f'Время операции {opr} непостоянно.png')





    def __str__(self):
        return (f'''
        ---------Маршрут {self.route}---------
        Всего людей {len(self.persons)}
        gg: {self.is_proverka()}
        Среднее выполнение: {self.avr_compl}
        Медиана выполнение: {self.mediana_vipol}
        Среднее выполнение операций: {' | '.join(["{}-{}ч".format(k, v) for k,v in self.avr_opr.items()])}
        Мединана операции: {' | '.join(["{}-{}ч".format(k, v) for k,v in self.mediana_opr.items()])}
        Кол-во проёбышей: {self.proebishi} {self.proebishi/len(self.persons)*100:.2f}%
        ---------------------------------------''')
