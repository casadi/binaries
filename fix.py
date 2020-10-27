
out = []

with open('./CMakeLists.txt','r') as f:
  replace = {"""option(SWIG_IMPORT "Export SWIG" OFF)""": """option(SWIG_IMPORT "Export SWIG" ON)""",
             """option(WITH_MATLAB "Compile the MATLAB front-end" OFF)""": """option(WITH_MATLAB "Compile the MATLAB front-end" ON)"""}
  for l in f.readlines():
    l = l.rstrip()
    if l in replace:
      r = replace[l]
      del replace[l]
      l = r
    out.append(l + "\n")
assert len(replace)==0

with open('./CMakeLists.txt','w') as f:
  for l in out:
    f.write(l)


