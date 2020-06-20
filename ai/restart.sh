#!/bin/bash
# demo: sh restart.sh io.wgengine.bkw100.com ai_id_1 1 1 2 101,10001 /ais/ai_1 match_id
ip=$1
ai_id=$2
room_id=$3
camp_id=$4
scenario_id=$5
seat_id=$6
path=$7
match_id=$8
cd $path
bash stop.sh $ai_id
bash start.sh $ip $ai_id $room_id $camp_id $scenario_id $seat_id $path
