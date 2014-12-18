import itertools
import sys
from collections import OrderedDict

def checkSector(edge):
	if mydict[edge[0]][edge[1]] == 'off':
		#print 'sector %s failed check at checkSector'%(edge)
		return(0)
	return(1)

def iterSectors(option,networkmap):
	#print "this is iterSectors. option is "+str(option)
	if len(option) <= 1: 
		return networkmap
	optstr=option[0]+option[1]
	found=0
	rev=optstr[::-1]
	try:
		blah=visited[optstr]
		found=1
		#we already have checked this sector. Pop and move on
		#print 'skipping pretested sector '+optstr
		option.pop(0)
		networkmap=iterSectors(option,networkmap)
		return networkmap
	except:
		donothing=1
	if not found:
		try:
			blah=visited[rev]
			found=1
			#we already have checked this sector. Pop and move on
			#print 'skipping pretested sector '+rev
			option.pop(0)
			networkmap=iterSectors(option,networkmap)
			return networkmap
		except:
			donothing=1

	if checkSector(optstr): #this simulates external checking.
		#print 'sector %s cleared a sector lookup'%(optstr)
		networkmap[option[0]][option[1]]='on'
		networkmap[option[1]][option[0]]='on'	
	else:
		#print 'sector %s failed a sector lookup'%(optstr)
		networkmap[option[0]][option[1]]='off'
		networkmap[option[1]][option[0]]='off'	

	#getting rid the start of what we just evaluated from option
	option.pop(0)
	visited[optstr]='yes'
	networkmap=iterSectors(option,networkmap)
	return networkmap

try:
	fp=open(sys.argv[1],'r')
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
		
for nodex,nodexval in mydict.iteritems():
	for nodey,nodeyval in nodexval.iteritems():
		print "%s%s -> %s"%(nodex,nodey,nodeyval)
nodestr=''
for node in nodes:
	nodestr+=node
options=itertools.permutations(nodestr,len(nodes))

optlist=list()
for option in options:
	if option[0]!=nodes[0]:
		continue
	optlist.append(list(option))
#print optlist
visited=dict()
for opt in optlist:
	networkmap=iterSectors(opt,networkmap)
print "Computed network map"
for nodex,nodexval in networkmap.iteritems():
	for nodey,nodeyval in nodexval.iteritems():
		print "%s%s -> %s"%(nodex,nodey,nodeyval)
	
#sys.exit(checkSector('ED'))
