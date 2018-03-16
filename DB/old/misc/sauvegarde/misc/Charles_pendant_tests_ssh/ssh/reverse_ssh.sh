###### INSTRUCTIONS #######
# This script will forward all ssh connections to AWS local host on port
# 2200 to the PI.
# To connect, simply connect to AWS via ssh, then connect again via ssh
# ssh -p 2200 imsi@localhost
############################


#! /bin/bash
ssh -i awspecan-proton-frankfurt.pem  -R 2200:localhost:22 ubuntu@18.196.165.106


