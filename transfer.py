from github3 import login, GitHubError
import datetime
import sys
import os

token = sys.argv[1]
commit = sys.argv[2]
full_commit = sys.argv[3]
release_name = sys.argv[4]

if not os.path.exists("assets"):
  os.makedirs("assets/")


repo_binaries=login('jgillis',token).repository('casadi','binaries')
repo_casadi=login('jgillis',token).repository('casadi','casadi')


def get_release(commit):
  for r in repo_binaries.releases():
    # These are artifacts
    if "commit-" + commit == r.tag_name:
      return r
    
  raise Exception("Not found")


try:
  release = repo_casadi.create_release(tag_name=release_name, name=release_name, target_commitish=full_commit, draft=True)
except GitHubError as error:
    print(error.errors)
    raise error


for a in get_release(commit).assets:
  print(a.name)
  name = a.name.replace(commit,"v"+release_name)
  assert a.download("assets/" + name)
  release.upload_asset(a.content_type, name, open("assets/" + name,"rb"))
