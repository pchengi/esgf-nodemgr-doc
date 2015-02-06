from time import sleep


from nodemgr.nodemgr.nodemap import NodeMap

nodemap_instance = NodeMap()

while (True):

    sleep(5)

    handle_tasks(nodemap_instance)
