#!/usr/bin/bash

echo "Arrêt de la sonde de récupération de données"
sonde_id=$(cat pid_sonde)
kill -9 $sonde_id

rm pid_sonde
