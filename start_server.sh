#!/usr/bin/bash

echo "Module de communication"
python -m webservice.webservice > log_webservice.txt 2>&1 &
comm_id=$!
echo $comm_id > pid_server

echo "Module de stockage"
python -m stockage.stockage > log_stockage.txt 2>&1 &
stock_id=$!
echo $stock_id >> pid_server

echo "Module de détection de crises"
python -m interface.crisis > log_crisis.txt 2>&1 &
crises_id=$!
echo $crises_id >> pid_server

#echo "Interface graphique"
#python -m interface.interface
#gui_id=$!
