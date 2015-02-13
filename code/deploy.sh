for n in `seq 1 6`; do
scp conf_examples/node_mgr_map.json greyworm$n:.
scp -r server greyworm$n:.
scp run_server.sh greyworm$n:.
done