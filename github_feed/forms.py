from django import forms

SQL_CHOICES = [
    ('sql_1', 'sql_1'),
    ('sql_2', 'sql_2'),
    ('sql_3', 'sql_3'),
    ('sql_4', 'sql_4'),
    ('sql_5', 'sql_5'),
]


class StatisticsForm(forms.Form):
    sql_query_num = forms.CharField(label="Выберите запрос:", widget=forms.Select(choices=SQL_CHOICES))
