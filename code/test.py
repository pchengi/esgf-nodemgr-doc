import itertools
import sys
from collections import OrderedDict

def checkSector(edge):
	global mydict
	if mydict[edge[0]][edge[1]] == 'off':
		#print 'sector %s failed check at checkSector'%(edge)
		return(0)
	return(1)

def iterSectors(option,networkmap):
	global timeunits
	#print "this is iterSectors. option is "+str(option)
	if len(option) <= 1: 
		return networkmap
	optstr=option[0]+option[1]
	fullopt=list(option)
	found=0
	rev=optstr[::-1]
	try:
		blah=visited[optstr]
		found=1
		#we already have checked this sector. Pop and move on
		#print 'skipping pretested sector '+optstr
		option.pop(0)
		if blah == 'off':
			while len(option) >=1:
				#print 'skipping check of node %s via %s. Full path was %s '%(option[0],optstr[0],fullopt)
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
			if blah == 'off':
				while len(option) >=1:
					#print 'skipping check of node %s via %s. Full path was %s '%(option[0],optstr[0],fullopt)
					option.pop(0)
			networkmap=iterSectors(option,networkmap)
			return networkmap
		except:
			donothing=1
	timeunits=timeunits+3
	print "External check for sector %s"%(optstr)
	if checkSector(optstr): #this simulates external checking.
		print 'sector %s cleared a sector lookup. Full path was %s'%(optstr,fullopt)
		networkmap[option[0]][option[1]]='on'
		networkmap[option[1]][option[0]]='on'	
	else:
		print 'sector %s failed a sector lookup'%(optstr)
		#if this is the first check, can abandon the next link check here
		networkmap[option[0]][option[1]]='off'
		networkmap[option[1]][option[0]]='off'	
		option.pop(0)
		while len(option) >=1:
			#print 'skipping check of node %s via %s. Full path was %s '%(option[0],optstr[0],fullopt)
			option.pop(0)
		visited[optstr]='off'
		return networkmap

	#getting rid the start of what we just evaluated from option
	option.pop(0)
	visited[optstr]='on'
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
	#print 'node is ~%s~'%(nodex)
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
	#print adj
	adjl=len(adj)
	x=adj[0]
	for y in range(1,adjl):
		if x == adj[y]:
			#print 'skipping with x %s and y %s'%(x,adj[y])
			continue
		#print 'turning on with x %s and y %s'%(x,adj[y])
		mydict[x][adj[y]]='on'
		
for nodex,nodexval in mydict.iteritems():
	for nodey,nodeyval in nodexval.iteritems():
		print "%s%s -> %s"%(nodex,nodey,nodeyval)
nodestr=''
for node in nodes:
	nodestr+=node
options=itertools.permutations(nodestr,3)

optlist=list()
for option in options:
	#if option[0]!=nodes[0]:
	#	continue
	found=0	
	for mem in option:
		if mem == nodes[0]:
			found = 1
			break
	if found == 1:
		if option[0] == nodes[0]:
			optlist.append(list(option))
			continue 
		continue #we only want the node to be in first position. Junk rest
	#not found current node. Prepend to list.
	mlist=list(nodes[0])
	for mem in option:
		mlist.append(mem)
		
	optlist.append(mlist)
#for opt in optlist:
#	print opt
print len(optlist)
timeunits=0
visited=dict()
for opt in optlist:
	#print opt
	networkmap=iterSectors(opt,networkmap)
print "Computed network map"
for nodex,nodexval in networkmap.iteritems():
	for nodey,nodeyval in nodexval.iteritems():
		print "%s%s -> %s"%(nodex,nodey,nodeyval)
print 'Total time units consumed:'+str(timeunits)	
#sys.exit(checkSector('ED'))
