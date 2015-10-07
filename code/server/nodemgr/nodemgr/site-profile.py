from time import time

PROPERTIES = "/esg/config/esgf.properties"
TYPE_FN = "/esg/config/config_type"


def ts_func():

    return str(int(time()*1000))

def parse_properties():

    pdict = {}

    f = open(PROPERTIES)

    pdict["timestamp"] = ts_func()
    for line in f:
        ll = line.strip()
        if ll[0] != '#':
            parts = line.split('=')
            pdict[ parts[0].strip() ] = parts[1].strip()

    f.close()

    f.open(TYPE_FN)
    val=f.read()
    pdict["node.type"] = val.strip()


    return pdict

def add_sn(pdict,sn):




def get_json(pdict):

    return 


def gen_reg_xml(arr_in):

    outarr =  ["<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n"]

    ts = ts_func()
    

    for z in arr:

        outarr.append("    <Node ")

        outarr.append('organization="' )
        outarr.append(x["esg.root.id"])
        outarr.append('" namespace="') 
        outarr.append(x["node.namespace"])
        outarr.append('" nodePeerGroup="')
        outarr.append(x["node.peer.group"]) 
        outarr.append('" supportEmail="')
        outarr.append(x["mail.admin.address"]) 
        outarr.append('" hostname="')
        outarr.append(x["esgf.host"]) 
        outarr.append('" ip="')
        outarr.append(x["esgf.host.ip"]) 
        outarr.append('" shortName="')
        outarr.append(x["node.short.name"]) 
        outarr.append('" longName="')
        outarr.append(x["node.long.name"]) 
        outarr.append('" timeStamp="')
# generated on properties file read
        outarr.append(x["timestamp"]) 
        outarr.append('" version="')
        outarr.append(x["version"]) 
        outarr.append('" release="')
        outarr.append(x["release"]) 
        outarr.append('" nodeType="')
        outarr.append(x["node.type"]) 
        outarr.append('" adminPeer="')
#  This should correspond to super-node for member-nodes
#  adjacent super-node for super-nodes
#        outarr.append(x["admin.peer"]) 
        outarr.append(x["default.peer"]) 
        outarr.append('" defaultPeer="')
        outarr.append(x["esgf.default.peer"]) 
#        outarr.append('" ="')
#        outarr.append(x[""]) 
        outarr.append('">\n')

# TODO: populate CA hash and correct endpoint
# for now uses the hostname
        outarr.append('        <CA hash="dunno" endpoint="')
        outarr.append(x["esgf.host"])
        outarr.append('" dn="dunno"/>\n')

        outarr.append('"       <GeoLocation lat="')
        outarr.append(x["node.geolocation.lat"])
        outarr.append('" lon="')
        outarr.append(x["node.geolocation.lon"])
        outarr.append('" city="')
        outarr.append(x["node.geolocation.city"])
        outarr.append('"/>\n')

        if "node.manager.service.endpoint" in x:
            outarr.append('        <NodeManager endpoint="')
            outarr.append(x["node.manager.service.endpoint"]) 
            outarr.append('"/>\n')

        if "orp.security.authorization.service.endpoint" in x:
            outarr.append('        <AuthorizationService endpoint="')
            outarr.append(x["orp.security.authorization.service.endpoint="]) 
            outarr.append('"/>\n')

        if  in x:
            outarr.append('" ="')
            outarr.append(x[""]) 
            outarr.append('">\n')


#        <OpenIDProvider endpoint="https://pcmdi9.llnl.gov/esgf-idp/idp/openidServer.htm"/>
#        <FrontEnd endpoint="http://pcmdi9.llnl.gov/esgf-web-fe/"/>
#        <IndexService port="8983" endpoint="http://pcmdi9.llnl.gov/esg-search/search"/>
#        <AttributeService endpoint="https://pcmdi9.llnl.gov/esgf-idp/saml/soap/secure/attributeService.htm">



#        outarr.append('" ="')
#        outarr.append(x[""]) 
        outarr.append('">\n')

#        outarr.append('" ="')
#        outarr.append(x[""]) 
        outarr.append('">\n')


        # <CA hash="dunno" endpoint="dapp2p.cccma.ec.gc.ca" dn="dunno"/>

        # <ThreddsService endpoint="http://dapp2p.cccma.ec.gc.ca/thredds"/>
        # <GridFTPService endpoint="gsiftp://dapp2p.cccma.ec.gc.ca">
        #     <Configuration serviceType="Replication" port="2812"/>
        #     <Configuration serviceType="Download" port="2811"/>
        # </GridFTPService>
        # <Metrics>
        #     <DownloadedData count="0" size="0" users="0"/>
        #     <RegisteredUsers count="0"/>
        # </Metrics>
        # <RelyingPartyService endpoint="https://dapp2p.cccma.ec.gc.ca/esg-orp/html.htm"/>
        # <PEMCert>
        #     <Cert>NOT_AVAILABLE</Cert>
        # </PEMCert>


        outarr.append("    </Node>\n")
