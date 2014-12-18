
from collections import OrderedDict

def load_dict(fn):

    try:
        fp=open(fn,'r')
    except:
        print "Couldn't open file"
        sys.exit(-1)
    lines=fp.readlines()
    numl=len(lines)
    nodes=lines[0].split('\n')[0].split(' ')
    mydict=OrderedDict()
    networkmap=OrderedDict()
    for nodex in nodes:
        print 'node is ~%s~'%(nodex)
        for nodey in nodes:
            if nodex == nodey:
                continue
            try:
                blah=mydict[nodex]
            except:
                mydict[nodex]=OrderedDict()
                networkmap[nodex]=OrderedDict()

            mydict[nodex][nodey]='off'
            networkmap[nodex][nodey]='on'
    return mydict