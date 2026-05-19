import sys
import json
import urllib.request
import re
from datetime import date

def get_commit_dates(repo, path, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    base_url = f"https://api.github.com/repos/{repo}/commits?path={path}&per_page=1"

    # Get last commit date
    req = urllib.request.Request(base_url, headers=headers)
    with urllib.request.urlopen(req) as r:
        commits = json.loads(r.read())
        last_date = commits[0]["commit"]["committer"]["date"][:10] if commits else str(date.today())

    # Get link header to find last page
    req2 = urllib.request.Request(base_url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(req2) as r:
            link = r.headers.get("Link", "")
    except:
        link = ""

    # Get first commit via last page
    first_date = last_date
    if 'rel="last"' in link:
        match = re.search(r'page=(\d+)>; rel="last"', link)
        if match:
            last_page = match.group(1)
            req3 = urllib.request.Request(
                f"{base_url}&page={last_page}",
                headers=headers
            )
            with urllib.request.urlopen(req3) as r:
                commits = json.loads(r.read())
                first_date = commits[0]["commit"]["committer"]["date"][:10] if commits else last_date

    print(f"{first_date},{last_date}")

if __name__ == "__main__":
    repo = sys.argv[1]
    path = sys.argv[2]
    token = sys.argv[3]
    get_commit_dates(repo, path, token)