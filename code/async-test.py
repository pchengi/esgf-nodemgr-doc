from threading import Thread

import test

finished = false

NNodes = 5

DELAY = 10

comm_table = []

for n in range(NNodes):

    comm_table.append(NNodes * [0])


def communicate(src, dest):

    comm_table


conv = ['A', 'B', 'C', 'D', 'E']

def poll_for_msg(my_num):


    while (not finished):

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
                        res = handle_req(va)
                        comm_table[][] = res

                            
def handle_req(my_num, pairs):
    

