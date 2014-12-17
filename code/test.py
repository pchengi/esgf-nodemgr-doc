import itertools
from collections import OrderedDict
fp=open('sync-inp1','r')
lines=fp.readlines()
numl=len(lines)
nodes=lines[0].split('\n')[0].split(' ')
mydict=OrderedDict()
for nodex in nodes:
	for nodey in nodes:
		if nodex == nodey:
			continue
		try:
			blah=mydict[nodex]
		except:
			mydict[nodex]=OrderedDict()
		mydict[nodex][nodey]='off'
for i in range(1,numl-1): 
	adj=lines[i].split('\n')[0].split(' ')
	adjl=len(adj)
	x=adj[0]
	for y in range(1,adjl-1):
		if x == adj[y]:
			continue
		mydict[x][adj[y]]='on'
		
for nodex,nodexval in mydict.iteritems():
	for nodey,nodeyval in nodexval.iteritems():
		print "%s%s -> %s"%(nodex,nodey,nodeyval)
options=itertools.combinations('ABCDE',2)

for option in options:
	print option
