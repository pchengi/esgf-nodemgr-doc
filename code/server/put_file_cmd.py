from user_api import put_file
import sys

from os.path import basename

application = sys.argv[1]

project = sys.argv[2] 

fpath = sys.argv[3]


f = open(fpath)

dat = f.read()

fname = basename(fpath)

put_file(application, project, fname, dat)





