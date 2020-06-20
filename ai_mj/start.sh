#!/bin/bash
# demo: sh start.sh io.wgengine.bkw100.com ai_id_1 1 1 2 101,10001 /ais/ai_1 match_id
ip=$1
ai_id=$2
room_id=$3
camp_id=$4
scenario_id=$5
seat_id=$6
path=$7
echo ip is $ip
echo ai_id is $ai_id
echo room_id is $room_id
echo camp_id is $camp_id
echo scenario_id is $scenario_id
echo seat_id is $seat_id
echo path is $path
cd $path
python demo_ai.py $ip $ai_id $room_id $camp_id $scenario_id $seat_id
