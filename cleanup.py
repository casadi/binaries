from github3 import login
import datetime
import sys

token = sys.argv[1]

repo=login('jgillis',token).repository('casadi','binaries')

for r in repo.iter_releases():
  # These are artifacts
  if "untagged" in r.tag_name:
    r.delete()

  # Older than 2 weeks?
  if r.created_at < datetime.datetime.now()-datetime.timedelta(days=14):
    r.delete()
