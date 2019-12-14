SQL_QUERIES = {
    'sql_1': 'SELECT '+\
'extract(MONTH FROM "commits_commits"."creation_date") as "month", '+\
'"commits_commits"."message", '+\
'"commits_commits"."github_id", '+\
'"developers_developers"."nickname", '+\
'count(*) '+\
'OVER (PARTITION BY extract(MONTH FROM "commits_commits"."creation_date") ORDER BY '+\
'"commits_commits"."creation_date") '+\
'FROM "commits_commitupdates" '+\
'JOIN "commits_commits" '+\
'ON ("commits_commitupdates"."commit_id" = "commits_commits"."id") '+\
'LEFT JOIN "commits_commits_developers" '+\
'ON ("commits_commits"."id" = "commits_commits_developers"."commits_id") '+\
'LEFT JOIN "developers_developers" '+\
'ON ("commits_commits_developers"."developers_id" = '+\
'"developers_developers"."id") '+\
'WHERE extract(YEAR FROM "commits_commits"."creation_date") = 2019 AND '+\
'"commits_commitupdates"."status" = false',
    'sql_2': 'SELECT nickname, round(avg_changed_files, 2) AS avg_changed_files FROM ( '+\
'SELECT DISTINCT "developers_developers"."nickname", '+\
'avg(array_length("commits_commits"."changed_files", 1)) '+\
'OVER (ORDER BY "developers_developers"."nickname") AS '+\
'avg_changed_files '+\
'FROM "commits_commitupdates" '+\
'JOIN "commits_commits" '+\
'ON ("commits_commitupdates"."commit_id" = '+\
'"commits_commits"."id") '+\
'LEFT JOIN "commits_commits_developers" '+\
'ON ("commits_commits"."id" = '+\
'"commits_commits_developers"."commits_id") '+\
'LEFT JOIN "developers_developers" '+\
'ON ("commits_commits_developers"."developers_id" = '+\
'"developers_developers"."id") '+\
'WHERE "commits_commitupdates"."status" = false '+\
') AS subtable ORDER BY avg_changed_files DESC',
    'sql_3': 'SELECT '+\
'"repositories_repositories"."name", '+\
'"repositories_repositories"."stars", '+\
'RANK() OVER (ORDER BY "repositories_repositories"."stars" DESC) pulse_rank '+\
'FROM "repositories_repositories" '+\
'JOIN "repositories_repositorysubscriptions" '+\
'ON ("repositories_repositories"."id" = '+\
'"repositories_repositorysubscriptions"."repository_id") '+\
'WHERE ("repositories_repositorysubscriptions"."user_id" = 1 AND '+\
'"repositories_repositorysubscriptions"."status" = True)',
    'sql_4': 'SELECT '+\
'nickname, '+\
'RANK() OVER (ORDER BY avg_msg_len DESC) AS narrow_rank '+\
'FROM '+\
'(SELECT '+\
'"developers_developers".nickname, '+\
'sum(length("commits_commits"."message")) / count(*) as avg_msg_len '+\
'FROM "commits_commitupdates" '+\
'JOIN "commits_commits" '+\
'ON ("commits_commitupdates"."commit_id" = "commits_commits"."id") '+\
'LEFT JOIN "commits_commits_developers" '+\
'ON ("commits_commits"."id" = "commits_commits_developers"."commits_id") '+\
'LEFT JOIN "developers_developers" '+\
'ON ("commits_commits_developers"."developers_id" = '+\
'"developers_developers"."id") '+\
'WHERE extract(YEAR FROM "commits_commits"."creation_date") = 2019 AND '+\
'"commits_commitupdates"."status" = false '+\
'GROUP BY "developers_developers".nickname) as foo',
    'sql_5': 'SELECT '+\
'name, '+\
'add / -del AS productivity, '+\
'RANK() OVER (ORDER BY add / -del) FROM '+\
'(SELECT '+\
'"repositories_repositories"."name", '+\
'("repositories_repositories"."pulse_stats" ->> \'additions\')::int AS add, '+\
'("repositories_repositories"."pulse_stats" ->> \'deletions\')::int AS del '+\
'FROM "repositories_repositories" '+\
'JOIN "repositories_repositorysubscriptions" '+\
'ON ("repositories_repositories"."id" = '+\
'"repositories_repositorysubscriptions"."repository_id") '+\
'WHERE ("repositories_repositorysubscriptions"."status" = True)) '+\
'AS subtotal',
}
