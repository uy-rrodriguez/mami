#!/usr/bin/bash

echo "Arrêt du module de crises"
stock_id=$(head -n1 pid_server)
kill -9 $stock_id

echo "Arrêt du module de stockage"
crises_id=$(head -n2 pid_server | tail -n1)
kill -9 $crises_id

echo "Arrêt du module de communication"
comm_id=$(head -n3 pid_server | tail -n1)
kill -9 $comm_id

rm pid_server
