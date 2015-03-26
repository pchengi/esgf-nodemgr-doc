import nodemgr.nodemgr.simplequeue
import os, json


#INSTALL Needed to setup empty json for bootstrapping

REPO_DIR_PATH = "/esg/config/node-mgr-repo.json"



def init():
    f = open(REPO_DIR_PATH)
    ret = json.loads(f.read())
    f.close()
    return ret

def write_out():

    outf = open(REPO_DIR_PATH, "w")
    
    dat = json.dumps(repo_obj, sort_keys=True, indent=4, separators=(',', ': '))

    outf.write(dat)
    outf.close()

    #  tasKQ migrate task

repo_obj = init()

# this gets called once per project

#  False if project already exists, True if entry created
def init_proj(project):

    for n in repo_obj["collection"]:

        if n["project"] == project:
            return False

    tmpd = {}
    tmpd["project"] = project
    tmpd["applications"] = []

   
    repo_obj["collection"].append(tmpd)
    
    write_out()



    path = repo_obj["root_path"] + "/" + project 



    try:
        os.mkdir(path)
    except:
        print "WARN: directory exists"

    return True

#  False if project not found
#  True if entry created
#  None if doesn't exist (test for boolean type)
def init_directory(application, project):

    found = False
    for n in repo_obj["collection"]:

        if n["project"] == project:

            found = True
            app_list = n["applications"]
            
            for x in app_list:

                if x["name"] == application:
                    return
            

            tmpd = {}
            tmpd["name"] = application
            tmpd["files"] = []
            
            app_list.append(tmpd)
    
    if not found:

        return False

    write_out()

    path = repo_obj["root_path"] + "/" + project + "/" + application

    os.mkdir(path)

    return True

    
# Returns empty string on success; error message string on failure
def put_file(application, project, name, data):
    

    path = repo_obj["root_path"]

    full_path = path + "/" + project + "/" + application + "/" + name
    version = 1

    for n in repo_obj["collection"]:
 
        found = False
        if n["project"] == project:
    
            for x in n["applications"]:
    
                print x
                if x["name"] == application:
                    
                    found = True
                    fs = x["files"]

                    if name in fs:
                        version = fs["version"]
                        version = version + 1

                    else:
                 
                        fs["version"] = version

                
                        fs["name"] = full_path
        
    if not Found:

        return "project/application missing"

    outfname = full_path + "." + str(version)

    outf = open(outfname, "w")
    
    outf.write(data)
    outf.close()

    write_out()
    
    return ""
                        


def get_latest(application, project, name):

    path = repo_obj["root_path"]

    version = 0

    for n in repo_obj["collection"]:
        
        if n["project"] == project:

            for x in n["applications"]:
    
                if x["name"] == application:
                    
                    fs = x["files"]

                    if name in fs:
                        version = fs["version"]
             

    if version == 0:
        return ""

    full_path = path + "/" + project + "/" + application + "/" + name + "." + str(version)

    f = open(full_path)

    data = f.read()
    f.close()

    return data
