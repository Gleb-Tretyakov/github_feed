from django.shortcuts import render
from github_client import scripts
from django.db import connection
from github_feed.forms import StatisticsForm
from github_feed.sql_queries import SQL_QUERIES


def dictfetchall(cursor):
    print(cursor.description)
    columns = [col[0] for col in cursor.description]
    return columns, [
        row
        for row in cursor.fetchall()
    ]


def my_custom_sql(sql_key):
    cursor = connection.cursor()

    sql = SQL_QUERIES[sql_key]
    cursor.execute(sql)
    columns, data = dictfetchall(cursor)
    return columns, data


def feed(request):
    commits = scripts.feed_for_user(request.user)
    return render(request, 'feed.html', {'commits': commits})


def statistics(request):
    headings, data = [], []
    if request.method == 'POST':
        form = StatisticsForm(request.POST)
        if form.is_valid():
            sql_key = form.cleaned_data.get('sql_query_num')
            headings, data = my_custom_sql(sql_key)
    else:
        form = StatisticsForm()
    return render(request, 'statistics.html', {'form': form, 'headings': headings, 'data': data})
