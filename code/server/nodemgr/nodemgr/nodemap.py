import json

MAPFILE = ""



class NodeMap():

    def __init__(self):

        self.nodemap = json.loads(MAPFILE)
        
        

    def num_members(x):

        return len(x["members"])

    def assign_node(node_name):

        

        ref = self.nodemap["membernodeds"]
        
        fewest = min(ref, key=num_members))

        


