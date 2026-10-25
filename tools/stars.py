"""Total GitHub stars for the profile badge: every non-fork repo under ZJU-REAL plus the lab's repos that live elsewhere.

Run from the repository root:  python3 tools/stars.py
Writes profile/assets/stars.json in the shields.io endpoint format; the README badge reads it via
https://img.shields.io/endpoint?url=<raw URL of that file>. A scheduled workflow refreshes it daily.
Set GITHUB_TOKEN to avoid the anonymous API rate limit.
"""
import json, os, urllib.request

ORG = 'ZJU-REAL'
EXTRA = [  # lab-led repositories hosted outside the organization
    'microsoft/JARVIS',  # HuggingGPT, TaskBench, EasyTool
]
OUT = 'profile/assets/stars.json'


def get(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'zju-real-stars'})
    if os.environ.get('GITHUB_TOKEN'):
        req.add_header('Authorization', 'Bearer ' + os.environ['GITHUB_TOKEN'])
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def org_stars():
    total, page = 0, 1
    while True:
        repos = get(f'https://api.github.com/orgs/{ORG}/repos?per_page=100&type=public&page={page}')
        total += sum(r['stargazers_count'] for r in repos if not r['fork'])
        if len(repos) < 100:
            return total
        page += 1


def short(n):
    return f'{n / 1000:.1f}k'.replace('.0k', 'k') if n >= 1000 else str(n)


org = org_stars()
extra = {full: get(f'https://api.github.com/repos/{full}')['stargazers_count'] for full in EXTRA}
total = org + sum(extra.values())
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w') as f:
    json.dump({'schemaVersion': 1, 'label': 'Stars', 'message': short(total), 'color': 'blue', 'namedLogo': 'github',
               'total': total, 'org': org, 'extra': extra}, f, indent=2)
    f.write('\n')
print(f'{ORG}: {org}  extra: {extra}  total: {total} ({short(total)})')
