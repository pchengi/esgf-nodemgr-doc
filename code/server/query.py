from sqlalchemy import create_engine

import os, json

has_db = False

db_engine = None

PASS_FN = '/esg/config/.esg_pg_pass'

def  init_db():
    
    if not os.path.exists(PASS_FN):
        return (False, None)
    
    f = open(PASS_FN)

    passwd = f.read().strip()
    
    db_str = ( 'postgresql://dbsuper:' + passwd + '@localhost:5432/esgcet')

    engine = create_engine(db_str)

    return True, engine




def execute_count_query(qstr):


    
    if not has_db:
        return 0

    result = db_engine.execute(qstr)

    val = 0

    for row in result:
        val = row

    return val


def get_user_count():
    return    execute_count_query('select count(*) from (select distinct firstname, middlname, lastname from esgf_security.user) as tmp') -1


def get_dl_bytes():

    return execute_count_query('select sum(xfer_size) from esgf_node_manager.access_logging where data_size = xfer_size and xfer_size > 0')


def get_dl_count():

    return execute_count_query('select count(*) from esgf_node_manager.access_logging where data_size = xfer_size and xfer_size > 0')


def get_dl_users():

    return execute_count_query('select count(distinct user_id) from esgf_node_manager.access_logging')


has_db, db_engine = init_db()


class QueryRunner(Thread):

    def __init__(self, fn, c):

        super(QueryRunner, self)._init()
        self.target_fn = fn
        self.esg_config = c
        

    def run(self):

        f = open(target_fn, "w")
        
        outdict = {}

        if self.esg_config.is_idp():
            outdict["users_count"] = get_user_count()

#        if self.esg_config.is_data():
            
        
