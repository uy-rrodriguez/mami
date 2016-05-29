#!/usr/bin/bash

echo "Module de communication"
python -m interface.crisis >/dev/null &
comm_id=$!
echo $comm_id > pid_server

echo "Module de stockage"
python -m interface.crisis >/dev/null &
stock_id=$!
echo $stock_id >> pid_server

echo "Module de détection de crises"
python -m interface.crisis >/dev/null &
crises_id=$!
echo $crises_id >> pid_server

#echo "Interface graphique"
#python -m interface.interface
#gui_id=$!
