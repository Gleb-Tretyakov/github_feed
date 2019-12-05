import json
from github import Github
from developers.models import Developers, DeveloperSubscriptions
from repositories.models import Repositories, RepositorySubscriptions
from commits.models import Commits, CommitUpdates
from developers.models import DeveloperSubscriptions


CLIENT_TOKEN = '9f559e6161467c6d3def530e70f154f4d4444133'
SEARCH_LIMIT = 5


def get_client(client_token):
    return Github(client_token)


def get_default_client():
    return get_client(CLIENT_TOKEN)


def dev_info(dev_obj, is_in_library=False):
    return {
        "nickname": dev_obj.login,
        "name": dev_obj.name if dev_obj.name else "Не указано",
        "email": dev_obj.email if dev_obj.email else "Отсутсвует",
        "url": dev_obj.url,
        "avatar_url": dev_obj.avatar_url,
        "is_in_library": is_in_library,
    }


def get_developer_info_by_nickname(nickname):
    return dev_info(get_default_client().get_user(nickname))


def get_developer_commits(nickname):
    LIMIT = 20
    qualifires={"committer-name": nickname, "author-name": nickname}
    response = get_default_client().search_commits("", sort="committer-date", order="desc", **qualifires)
    commits = []
    for i, commit in enumerate(response):
        if i > LIMIT:
            break
        commits.append(commit)
    return commits


def add_developers_to_commits(commit_obj, developers):
    for developer in developers:
        if developer and developer.login:
            nickname = developer.login
            developer = get_or_create_developer(nickname)
            commit_obj.developers.add(developer)


def add_commits_to_updates(user, developer, commits):
    for commit in commits:
        commit_obj = Commits.get_or_none(github_id=commit.html_url)
        print(commit.commit.committer.date)
        if commit_obj is None:
            commit_obj = Commits.objects.create(
                message=commit.commit.message,
                creation_date=commit.commit.committer.date,
                changed_files=[file.filename for file in commit.files],
                github_id=commit.html_url
            )
            add_developers_to_commits(commit_obj, [commit.author])

        commit_obj.developers.add(developer)
        CommitUpdates.objects.get_or_create(user=user, commit=commit_obj)


def add_developer_to_user(nickname, user):
    developer = get_or_create_developer(nickname)

    commits = get_developer_commits(nickname)
    add_commits_to_updates(user, developer, commits)

    DeveloperSubscriptions.objects.update_or_create(user=user, developer=developer, defaults={'status': True})


def delete_developer_from_user(developer_nickname, user):
    developer = Developers.get_or_none(nickname=developer_nickname)
    if developer is None:
        return
    try:
        pref = DeveloperSubscriptions.objects.get(user=user, developer=developer)
        pref.status = False
        pref.save()
    except DeveloperSubscriptions.DoesNotExist:
        pass
    for commit in Commits.objects.filter(developers=developer):
        try:
            CommitUpdates.objects.filter(user=user, commit=commit).delete()
        except Exception:
            pass


def developer_subscriptions_of_user(user):
    try:
        developers = DeveloperSubscriptions.objects.filter(user=user, status=True).values(
            'developer__nickname',
            'developer__avatar_url',
            'developer__email',
            'developer__name'
        )
        answer = []
        print(developers)
        for developer in developers:
            answer.append({
                'nickname': developer['developer__nickname'],
                'avatar_url': developer['developer__avatar_url'],
                'email': developer['developer__email'],
                'name': developer['developer__name']
            })
        return answer
    except Exception:
        return []


def get_or_create_developer(nickname):
    info = get_developer_info_by_nickname(nickname)
    dev = Developers.get_or_none(nickname=nickname)
    if dev:
        return dev
    return Developers.objects.create(
        nickname=nickname,
        avatar_url=info["avatar_url"],
        email=info["email"],
        name=info["name"]
    )


def stats_info(repo_obj):
    freq_obj = repo_obj.get_stats_code_frequency()
    a = 0
    d = 0
    if freq_obj is not None:
        for item in freq_obj:
            a += item.additions
            d += item.deletions
    return {
        "additions": a,
        "deletions": d
    }


def repo_info(repo_obj, is_in_library):
    stats_contributors = repo_obj.get_stats_contributors()
    return {
        "name": repo_obj.name,
        "stars": len(repo_obj.get_stargazers()),
        "url": repo_obj.contents_url,
        "pulse_stats": stats_info(repo_obj),
    }


# search by occurrences in login
def search_developer(user, query):
    if not query:
        return []
    qualifiers = {"in": "login"}
    response = get_default_client().search_users(query.strip(), sort="joined", **qualifiers)
    answer = []
    for obj in response:
        is_in_library = False
        dev = Developers.get_or_none(nickname=obj.login)
        if dev and dev in user.developer_subscribes.filter(developersubscriptions__status=True):
            is_in_library = True
        answer.append(dev_info(obj, is_in_library))
        if len(answer) >= SEARCH_LIMIT:
            break
    return answer


# search by occurrences in name
def search_repo(user, query):
    qualifiers = {"in": "name"}
    resp = get_default_client().search_repositories(query.strip(), sort="joined", **qualifiers)
    answer = []
    for obj in resp:
        is_in_library = False
        repo = Repositories.get_or_none(git_id=obj.id)
        if repo and repo in user.repository_subscribes.filter(repository_subscribes__status=True):
            is_in_library = True
        answer.append(repo_info(obj, is_in_library))
        if len(answer) >= SEARCH_LIMIT:
            break
    # print(users)
    return users


def feed_for_user(user):
    return _feed_by_developers_for_user(user)


def _get_info_from_commit(commit):
    return {
        'status': commit['status'],
        'message': commit['commit__message'],
        'commit_url': commit['commit__github_id'],
        'creation_date': commit['commit__creation_date'],
        'changed_files': commit['commit__changed_files'],
        'developer_names': commit['commit__developers__nickname']
    }


def _feed_by_developers_for_user(user):
    try:
        commits = CommitUpdates.objects.filter(user=user).order_by('-commit__creation_date').values(
            'status',
            'commit__message',
            'commit__github_id',
            'commit__changed_files',
            'commit__creation_date',
            'commit__developers__nickname'
        )
    except Exception as ex:
        print(ex)
        return []
    answer = []
    for commit in commits:
        answer.append(_get_info_from_commit(commit))
    return answer
