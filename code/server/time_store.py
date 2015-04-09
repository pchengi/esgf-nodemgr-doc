
class TimeStore():

    def __init__():
        self.filename = ""
        self.ts = 0

    def write():
        
        outf = open(self.filename, "w")
        outf.write(str(self.ts))
        outf.close()


    def restore():
        inf = open(self.filename)
        x = inf.read()
        
        self.ts = int(x)
        inf.close()
    
    
ts_instance = TimeStore()

def get_instance():
    return ts_instance

