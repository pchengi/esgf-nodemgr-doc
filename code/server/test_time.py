import sys
import json

from nodemgr.nodemgr.site_profile import ts_func

from httplib import HTTPConnection as Conn

def get_time_lag(host):

    st = float(ts_func())

    conn = Conn(host, 80, timeout=10)
    conn.request("GET", "/esgf-nm/health-check-api?what=timestamp")
    resp = conn.getresponse()
                
    data_str = resp.read()

    dobj = json.loads(data_str)

    remote_t = float(dobj["ts_all"])

    edt = float(ts_func())


    drift = ((st + edt ) / 2 ) - remote_t

    return drift

print get_time_lag(sys.argv[1])
    
