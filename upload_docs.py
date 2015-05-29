import subprocess
from glob import iglob, glob
from shutil import copy, copyfile
from os.path import join, split

import sys
import os

import fileinput

hashversion = sys.argv[1]

release = "builds/"+hashversion
def rsync(source,dest):
  p = subprocess.Popen(["rsync","-avP","--delete","-e","ssh"] + glob(source) + ["casaditestbot,casadi@web.sourceforge.net:/home/groups/c/ca/casadi/htdocs/" + dest],bufsize=0)
  p.wait()

for line in fileinput.input("api/html/search/search.js", inplace = True):
  sys.stdout.write(line.replace("dbLocation", "\"../htdocs/%s/api/html/doxysearch.db\"" % release))

for line in fileinput.input("api/internal/search/search.js", inplace = True):
  sys.stdout.write(line.replace("dbLocation", "\"../htdocs/%s/api/internal/doxysearch.db\"" % release))
  
p = subprocess.Popen(["sftp","casaditestbot,casadi@web.sourceforge.net:/home/groups/c/ca/casadi/htdocs/"],stdin=subprocess.PIPE)
p.communicate(input="mkdir builds\nmkdir %s\nmkdir %s/api\nmkdir %s/tutorials\nmkdir %s/users_guide\nmkdir %s/cheatsheets\nmkdir %s/users_guide/html" % (releasedir,releasedir,releasedir,releasedir,releasedir,releasedir))
rsync("api/html","%s/api/" % release)  
rsync("api/internal","%s/api/" % release)  
file('tutorials/python/pdf/.htaccess','w').write("Options +Indexes")
rsync("tutorials/python/pdf/","%s/tutorials/" % release)  
p = subprocess.Popen(["sftp","casaditestbot,casadi@web.sourceforge.net:/home/pfs/project/c/ca/casadi/CasADi"],stdin=subprocess.PIPE)
p.communicate(input="cd %s\nput example_pack/example_pack.zip\n" % (releasedir))
rsync("users_guide/*.pdf","%s/users_guide/" % release)
rsync("users_guide/casadi-users_guide/","%s/users_guide/html" % release)
rsync("cheatsheet/*.pdf","%s/cheatsheets/" % release)
