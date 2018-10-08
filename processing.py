import pandas as pd


def check_sparsity(d):
    d_min = min(d)
    d_max = max(d)
    d_len = len(d)
    return f'Начальная дата {d_min}, конечная дата {d_max}, всего замеров {d_len}, ' \
           f'среднее время одного замера {abs(d_min-d_max)/d_len}'


def get_data_summary(d):
    s1 = len(d)
    s2 = len(d.columns)
    d_min = min(d['date'])
    d_max = max(d['date'])
    return f'Количество строк данных: {s1}\nКоличество столбцов данных: {s2}\nНачальная дата {d_min}, ' \
           f'конечная дата {d_max}, всего замеров {s1}, \nсреднее время одного замера {abs(d_min-d_max)/s1}'