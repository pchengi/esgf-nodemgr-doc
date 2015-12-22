T=0

sleeptime=60

src=/esg/config/esgf_nodemgr_map.json

while true ; do

    cp src snap.$T

    T=$(( $T + 1 ))

    sleep $sleeptime

    done







