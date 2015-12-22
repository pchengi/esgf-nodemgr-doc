MAX=$1

i=0

fn=

while [ $i -lt $MAX ] ; do

    nxt=$(( $i + 1))

    diff snap.$i snap.$nxt > snap.diff.$i


    i=$nxt

done 

