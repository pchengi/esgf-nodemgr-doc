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
    
    dat = json.dumps(repo_obj)

    outf.write(dat)
    outf.close()

    #  tasKQ migrate task

repo_obj = init()

# this gets called once per project

def init_proj(project):
    tmpd = {}
    tmpd["project"] = project
    tmpd["applications"] = []
   
    repo_obj["collection"].append(tmpd)
    
    write_out()

    

def init_directory(application, project):

    for n in repo_obj:
        if n["project"] == project:

            app_list = n["applications"]
            
            tmpd = {}
            tmpd["name"] = application
            tmpd["files"] = []
            
            app_list.append(tmpd)
    write_out()

    

    

def put_file(application, project, name, data):
    

    path = repo_obj["root_path"]

    full_path = path + "/" + project + "/" + application + "/" + name
    version = 1

    for n in repo_obj["collection"]:
        
        if n["project"] == project:

            for x in n["applications"]:
    
                if x["name"] == application:
                    
                    fs = x["files"]

                    if name in fs:
                        version = fs["version"]
                        version = version + 1

                    else:
                 
                        fs["version"] = version

                
                        fs["name"] = full_path
        

    outfname = full_path + "." + str(version)

    outf = open(outfname, "w")
    
    outf.write(data)
    outf.close()

    write_out()

                        


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

    full_path = path + "/" project + "/" + application + "/" + name + "." + str(version)

    f = open(full_path)

    data = f.read()
    f.close()

    return data
