#!/bin/bash



ch01=212.129.38.224   #   challenge01.root-me.org
ch03=212.129.38.224   #   challenge03.root-me.org
irc_host=irc.root-me.org

build_cmd ()
{
  param=$1
  host=${param%:*}
  port=${param#*:}
  ssh_param="${ssh_param} -L ${port}:${host}:${port}"
}

# www 
#ssh_param="-L 8080:${ch01}:443"
ssh_param=""

# VNC to AWS
build_cmd "localhost:5909"

#build_cmd "${ch01}:80"

# SSH to root-me
build_cmd "${ch03}:2222"
build_cmd "${ch03}:2223"
build_cmd "${ch03}:2224"
build_cmd "${ch03}:56538"
build_cmd "${ch03}:56543"
build_cmd "${ch03}:56544"
build_cmd "${ch03}:61056"
# IRC to root-me
build_cmd "${irc_host}:6667"

#ssh -i ~/.ssh/awspecan-lex-london.pem ${ssh_param} -N ${user}@${gw}
# vncviewer : protonmail
ssh ${ssh_param} -N ubuntu

