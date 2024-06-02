from requests import get
from datetime import datetime


def get_public_github_data(user_name: str, github_token:str):
    URL = f"https://api.github.com/user/repos"
    header = {
        # "Authorization": f"token {TOKEN}",
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = get(url=URL.format(user_name=user_name), headers=header)
    holder = []
    if data.ok:
        data = data.json()
        for repo in data:
            if repo.get("owner", {}).get("login") != user_name:
                continue
            if repo['language'] is None:
                continue
            language_url = repo['languages_url']
            languages = get(language_url, headers=header)
            if languages.ok:
                languages = languages.json()
            else:
                languages = {}

            response = dict(
                name=repo['name'],
                private=repo['private'],
                description=repo['description'],
                size=repo['size'],
                languages=languages,
                shield_logo=list(map(language_shield_converted, languages)),
                url=repo['html_url'],
                created_at=datetime.fromisoformat(repo['created_at']).strftime("%d-%m-%Y"),
            )
            holder.append(response)
    return holder


def language_shield_converted(language: str):
    language = language.lower().strip()
    if language == "jupyter notebook":
        language = "jupyter"
    if language in ["shell", 'gnu']:
        language = "gnubash"
    if language == "c++":
        language = "cpp"
    if language == "html":
        language = "html5"
    if language == "css":
        language = "css3"
    return language
