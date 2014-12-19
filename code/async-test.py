from threading import Thread

import sys

import loader

inf = sys.argv[1]

mydict = loader.load_dict(inf)


finished = False

NNodes = 5

DELAY = 10

comm_table = []

for n in range(NNodes):

    comm_table.append(NNodes * [0])



conv = ['A', 'B', 'C', 'D', 'E']

def check_table(my_num):

        # iterate through all nodes for messages
        
        for n in range(NNodes):

            if (not n == my_num):

                if not comm_table[n][my_num] == 0:

                    val = comm_table[n][my_num]
                    comm_table[n][my_num] = 0


# check if communication is ok

                    x = conv[n]
                    y = conv[my_num]
                    
                    if mydict[x][y] == "off":
                        print "sleep", DELAY
                    else:
                        # send ack
                        if len(val[0]) > 0:
                            res = handle_req(my_num, val)
                        else:
                            res = "ack"
                        comm_table[my_num][n] = res

def poll_for_msg(my_num):


    while (not finished):

        check_table(my_num)

    print my_num, " Exiting"

def handle_req(my_num, pairs):

    
    #    print pairs
    
    # handle delegation of tasks if necessary

    outgroups = {}
    
    for m in pairs[0]:
        
        
        outgroups[m[1]] = []
    
    if len(pairs[1]) > 0:
    

    

                
        for n in pairs[1]:
            
            for m in pairs[0]:

                if m[1] == n[0]:
                    #                    assert (outgroups[m[1]][0]== m[1])
                    outgroups[m[1]].append(n)

#    print outgroups
    results = []
    unreachable = []
                        
    for z in pairs[0]:

        dest = z[1]
        val = outgroups[dest]
    
        comm_table[my_num][dest] = [val, []]
        check_table(dest)
        
        res = comm_table[dest][my_num]
        
        if res == 0:
            print my_num, dest, 0
            unreachable.append(val)
        
        else:
            print my_num, dest, 1
                
        comm_table[dest][my_num] = 0
        
        results.append(res)

    return results, unreachable



# coordinator code goes here

# make the pairs

pairs = []

for i in range(NNodes):

    for j in range(i+1, NNodes):


        pairs.append([i,j])

print pairs

#print mydict



adj_req = pairs[0:NNodes-1]
remote_req = pairs[NNodes-1:]

active = {}

total = 10

count = 0

while not finished:


    
    res, unr = handle_req(0, [adj_req, remote_req])

    todos = []
    for x, y, z in zip(adj_req, res, unr):
        todos = todos + z
        
        if not y == 0:
            active[x[1]] = 1
            count += 1
            count += len(y)

    if count == total:
        finished = True
        continue

    adj_req = []
    remote_req = []

    for n in active:
        remote_tmp  = []

        for m in todos:
            if m[1] == n:
                remote_tmp.append([n, m[0]])
        
        if len(remote_tmp) > 0:
            adj_req.append([0, n])
            remote_req = remote_req + remote_tmp

    missed = []

    for n in todos:
        found = False
        for m in remote_req:

            if n == m:
                found = True
                break
        if found == True:
            missed.append(n)


    if len(remote_req) ==0:
        finished = True

#    remote_req.append(missed)
# TODO:  optimize for missing node(s) case

print res



