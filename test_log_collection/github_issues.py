#!/usr/bin/env python3

# The script requires the PyGitHub module and github token stored in the .creds file

from github import Github
import json

with open('.creds') as o:
    gh = Github(o.readline().strip("\n"))

# Two random clients to show that the scripts work
repos = [
    "ethereum/go-ethereum",
    "erigontech/erigon",
    ]

issues = {}
for name in repos:
    repo = gh.get_repo(name)
    issues[name] = []
    for issue in repo.get_issues():
        temp_dict = {}
        temp_dict['subject'] = issue.title
        temp_dict['data'] = issue.raw_data
        temp_dict['comments'] = []
        if issue.comments > 0:
            for comment in issue.get_comments():
                temp_dict['comments'].append(comment.raw_data)
        issues[name].append(temp_dict)


with open('test.json', 'w') as file:
    file.write(json.dumps(issues))
