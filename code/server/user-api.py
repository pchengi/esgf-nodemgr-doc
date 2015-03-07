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
    tmpd["applications"] = {}
   
    repo_obj.append(tmpd)
    
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

    
    

def get_path(application, project, name):

    return
