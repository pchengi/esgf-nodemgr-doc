
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
    for i in range(1,numl):
        adj=lines[i].split('\n')[0].split(' ')
        print adj
        adjl=len(adj)
        x=adj[0]
        for y in range(1,adjl):
            if x == adj[y]:
                print 'skipping with x %s and y %s'%(x,adj[y])
                continue
		#print 'turning on with x %s and y %s'%(x,adj[y])
            mydict[x][adj[y]]='on'
    return mydict