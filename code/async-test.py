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
                        sleep(DELAY)
                    else:
                        # send ack
                        if len(val) > 0:
                            res = handle_req(my_num, val)
                        else:
                            res = "ack"
                        comm_table[my_num][n] = res

def poll_for_msg(my_num):


    while (not finished):

        check_table(my_num)

    print my_num, " Exiting"

def handle_req(my_num, pairs):

    outgroups = []
    
    
    
    # handle delegation of tasks if necessary
    
    if len(pairs[1]) > 0:
    
        for m in pairs[0]:
        
            outgroups.append([m[1]])
        
        for n in pairs[1]:
            for m in pairs[0]:

                if m[1] == n[0]:
                    assert (outgroups[m[1]][1] == m[1])
                    outgroups[m[1]].append(n)
    results = []

    for z, n in pairs[0], outgroups:

        comm_table[my_num][z[1]] = n[1:]
        check_table(z[1], [n[1:], []])
        
        res = comm_table[n[1], my_num]
        comm_table[n[1], my_num] = 0
        
        results.append(res)

    return results









# coordinator code goes here

# make the pairs

pairs = []

for i in range(NNodes):

    for j in range(i+1, NNodes):


        pairs.append([i,j])

print pairs

res = handle_req(0, [pairs[0:NNodes], pairs[NNodes:]])


print res



