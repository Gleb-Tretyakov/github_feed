import json
from github import Github
from developers.models import Developers, DeveloperSubscriptions
from repositories.models import Repositories, RepositorySubscriptions
from commits.models import Commits, CommitUpdates
from developers.models import DeveloperSubscriptions
from branches.models import Branches


CLIENT_TOKEN = '9f559e6161467c6d3def530e70f154f4d4444133'
SEARCH_LIMIT = 5
COMMITS_LIMIT = 20


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
        "is_in_library": is_in_library
    }


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


def repo_info(repo_obj, is_in_library=False):
    return {
        "name": repo_obj.full_name,
        "stars": repo_obj.get_stargazers().totalCount,
        "pulse_stats": stats_info(repo_obj),
        "branches": [branch.name for branch in repo_obj.get_branches()[:5]],
        "is_in_library": is_in_library
    }


def get_developer_info_by_nickname(nickname):
    return dev_info(get_default_client().get_user(nickname))


def get_repository_info_by_name(repo_name):
    return repo_info(get_default_client().get_repo(repo_name))


def get_developer_commits(nickname):
    qualifires = {"committer-name": nickname, "author-name": nickname}
    response = get_default_client().search_commits("", sort="committer-date", order="desc", **qualifires)
    commits = []
    for i, commit in enumerate(response):
        if i > COMMITS_LIMIT:
            break
        commits.append(commit)
    return commits


def get_repository_commits(repo_name):
    repo_obj = get_default_client().get_repo(repo_name)
    commits = sorted(repo_obj.get_commits(), key=lambda c: c.commit.committer.date)
    commits.reverse()
    return commits[:COMMITS_LIMIT]


def add_developers_to_commits(commit_obj, developers):
    for developer in developers:
        if developer and developer.login:
            nickname = developer.login
            developer = get_or_create_developer(nickname)
            commit_obj.developers.add(developer)


def add_commits_to_updates(user, commits, developer=None, repository=None):
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

        if developer:
            commit_obj.developers.add(developer)
        if repository:
            commit_obj.repository.add(repository)

        CommitUpdates.objects.get_or_create(user=user, commit=commit_obj)


def add_developer_to_user(nickname, user):
    developer = get_or_create_developer(nickname)

    commits = get_developer_commits(nickname)
    add_commits_to_updates(user, commits, developer, None)

    DeveloperSubscriptions.objects.update_or_create(user=user, developer=developer, defaults={'status': True})


def add_repository_to_user(repo_name, user):
    repository = get_or_create_repository(repo_name)

    commits = get_repository_commits(repo_name)
    add_commits_to_updates(user, commits, None, repository)

    RepositorySubscriptions.objects.update_or_create(user=user, repository=repository, defaults={'status': True})


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


def delete_repository_from_user(repository_name, user):
    repository = Repositories.get_or_none(name=repository_name)
    if repository is None:
        return
    try:
        pref = RepositorySubscriptions.objects.get(user=user, repository=repository)
        pref.status = False
        pref.save()
    except RepositorySubscriptions.DoesNotExist:
        pass
    for commit in Commits.objects.filter(repository=repository):
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


def repository_subscriptions_of_user(user):
    try:
        repositories = RepositorySubscriptions.objects.filter(user=user, status=True).values(
            'repository__name',
            'repository__stars',
            'repository__pulse_stats',
            'repository__branches__name'
        )
        print(repositories)
        answer = []
        for repository in repositories:
            answer.append({
                'name': repository['repository__name'],
                'stars': repository['repository__stars'],
                'pulse_stats': repository['repository__pulse_stats'],
                'branches': repository['repository__branches__name']
            })
        return answer
    except Exception as e:
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


def get_or_create_branch(name):
    br = Branches.get_or_none(name=name)
    if br:
        return br
    return Branches.objects.create(name=name)


def get_or_create_repository(name):
    info = get_repository_info_by_name(name)
    repo = Repositories.get_or_none(name=name)
    if repo:
        return repo
    repository = Repositories.objects.create(
        name=name,
        stars=info["stars"],
        pulse_stats=info["pulse_stats"],
    )
    for branch in info["branches"]:
        repository.branches.add(get_or_create_branch(branch))
    return repository


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
def search_repository(user, query):
    if not query:
        return []
    qualifiers = {"in": "name"}
    resp = get_default_client().search_repositories(query.strip(), sort="stars", **qualifiers)
    answer = []
    for obj in resp:
        print(obj.full_name)
        is_in_library = False
        repo = Repositories.get_or_none(name=obj.full_name)
        if repo and repo in user.repository_subscribes.filter(repositorysubscriptions__status=True):
            is_in_library = True
        answer.append(repo_info(obj, is_in_library))
        if len(answer) >= SEARCH_LIMIT:
            break
    return answer


def _get_info_from_commit(commit):
    return {
        'status': commit['status'],
        'message': commit['commit__message'],
        'commit_url': commit['commit__github_id'],
        'creation_date': commit['commit__creation_date'],
        'changed_files': commit['commit__changed_files'],
        'developer_names': commit['commit__developers__nickname']
    }


def feed_for_user(user):
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
