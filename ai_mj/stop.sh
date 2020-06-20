#!/bin/bash
# demo bash kill.sh ai_id_1
NAME=$1
echo kill  $NAME
ID=`ps -ef | grep "$NAME" | grep -v "$0" | grep -v "grep" |grep -v "restart"| awk '{print $2}'`
echo  process id is $ID
for id in $ID 
do
kill -9 $id 
echo "killed $id"
done
echo "done"
