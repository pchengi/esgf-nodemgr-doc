import itertools
from collections import OrderedDict
fp=open('inp1','r')
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
print numl
for nodex,nodexval in mydict.iteritems():
	for nodey,nodeyval in nodexval.iteritems():
		print "%s%s -> %s"%(nodex,nodey,nodeyval)
options=itertools.combinations('ABCDE',2)

for option in options:
	print option
