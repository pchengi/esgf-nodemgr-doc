import os


def self_check(datanode):

    if datanode:
        #get roots somehow
        res = storage_health()
    



def storage_health(tds_roots):


    
    for pth in tds_roots:
        avail True
        try:
            os.stat()
        except:
            avail = False
