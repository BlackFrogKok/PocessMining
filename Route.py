from datetime import timedelta
from statistics import median

def sec(dt):
    return [i.total_seconds() / 3600 for i in dt]

def hours(dt):
    return dt.total_seconds() / 3600

def _render_opr_and_compl_time(persons, obedinenie):
    buffer = {}
    buffer_date = {}
    time_vipols_list = []
    proebishi = 0
    for person in persons:
        time_vipols_list.append(hours(person.time_vipol))
        if person.is_over_limit():
            proebishi += 1
        for opr, time in person.opr_time.items():
            if opr in buffer:
                buffer[opr] += sec(time)
            else:
                buffer[opr] = sec(time)
        for opr, time in person.opr_start_date.items():
            if opr in buffer:
                buffer_date[opr] += [(time[i], opr.opr_time[opr][i]) for i in range(len(opr.opr_time[opr]))]
            else:
                buffer_date[opr] = [(time[i], opr.opr_time[opr][i]) for i in range(len(opr.opr_time[opr]))]
    if obedinenie:
        buffer['4+1'] = []
        for i in range(len(buffer['4'])):
            buffer['4+1'].append(buffer['4'][i] + buffer['1'][i] + buffer['0'][i])
    return buffer, buffer_date, time_vipols_list, proebishi



class Route:
    def __init__(self, route, persons, func=lambda x: x, obedinenie=False):
        self.route = route
        self.persons = list(filter(func, persons))
        #self.opr_time, self.opr_date, time_vipols_list, self.proebishi = _render_opr_and_compl_time(self.persons, obedinenie)
        # self.avr_compl = sum([hours(i.time_vipol) for i in self.persons]) / len(self.persons)
        #self.mediana_vipol = median(time_vipols_list)
        #self.avr_opr, self.mediana_opr = self._render_avr_mediana_opr()
        #self.fraction = {k:(v / sum(self.avr_opr.values())) for k, v in self.avr_opr.items()}
        #self.max_fraction_opr = max(self.fraction, key=self.fraction.get)
        #self.dev_opr = self._render_deviation()
        
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
