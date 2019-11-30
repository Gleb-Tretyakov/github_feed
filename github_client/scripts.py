from github import Github
from developers.models import Developers, DeveloperSubscriptions
from repositories.models import Repositories, RepositorySubscriptions


CLIENT_TOKEN = '9f559e6161467c6d3def530e70f154f4d4444133'
SEARCH_LIMIT = 5


def get_client(client_token):
    return Github(client_token)


def get_default_client():
    return get_client(CLIENT_TOKEN)


def get_developer_info(developer_id):
    pass


def get_developers_commits(developer_id):
    pass


def add_developer_to_user(developer_id, user):
    developer = Developers.get_or_none(id=developer_id)
    if developer is None:
        info = get_developer_info(developer_id)
        developer = Developers.objects.create(
            nickname=info['nickname'],
            avatar_url=info['avatar_url'],
            git_id=info['git_id'],
        )

    commits = get_developers_commits(developer_id)
    add_commits_to_updates(user, developer, commits)

    DeveloperSubscriptions.objects.update_or_create(person=user, developer=developer, defaults={'status': True})


def delete_developer_from_user():
    pass


def preferences_of_user():
    pass


def get_developer(name):
    resp_dev = get_default_client().get_user(name)
    dev = Developers.get_or_none(id=resp_dev.id)
    if dev:
        return dev
    return Developers.objects.create(
        id=resp_dev.id,
        nickname=resp_dev.login,
        avatar_url=resp_dev.avatar_url,
    )


def dev_info(dev_obj, is_in_library):
    return {
        "nickname": dev_obj.login,
        "name": dev_obj.name,
        "email": dev_obj.email,
        "git_id": dev_obj.id,
        "url": dev_obj.url,
        "avatar_url": dev_obj.avatar_url,
        "is_in_library": is_in_library,
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
    qualifiers = {"in": "login"}
    resp = get_default_client().search_users(query.strip(), sort="joined", **qualifiers)
    answer = []
    for obj in resp:
        is_in_library = False
        dev = Developers.get_or_none(git_id=obj.id)
        if dev and dev in user.developer_subscribes.filter(developer_subscribes__status=True):
            is_in_library = True
        answer.append(dev_info(obj, is_in_library))
        if len(answer) >= SEARCH_LIMIT:
            break
    # print(answer)
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