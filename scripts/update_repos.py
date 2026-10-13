"""Обновляет блок «Репозитории» в README профиля списком публичных репозиториев."""
import json
import os
import re
import urllib.request

USER = os.environ.get("GH_USER", "StanislavTark")
TOKEN = os.environ.get("GITHUB_TOKEN")
README = "README.md"
START, END = "<!-- REPOS:START -->", "<!-- REPOS:END -->"

req = urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed&type=owner",
    headers={"Accept": "application/vnd.github+json",
             **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})},
)
with urllib.request.urlopen(req) as r:
    repos = json.load(r)

rows = ["| Репозиторий | Описание | Язык | Обновлён |", "| --- | --- | --- | --- |"]
for repo in repos:
    if repo["fork"] or repo["archived"] or repo["name"].lower() == USER.lower():
        continue
    desc = (repo["description"] or "—").replace("|", "\\|")
    lang = repo["language"] or "—"
    pushed = repo["pushed_at"][:10]
    rows.append(f"| [{repo['name']}]({repo['html_url']}) | {desc} | {lang} | {pushed} |")

block = f"{START}\n" + "\n".join(rows) + f"\n{END}"
text = open(README, encoding="utf-8").read()
new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
if new != text:
    open(README, "w", encoding="utf-8").write(new)
    print("README обновлён")
else:
    print("Изменений нет")
