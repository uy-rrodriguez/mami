#!/usr/bin/bash

echo "Sonde de récupération de données"
python -m sonde.sonde >/dev/null &
sonde_id=$!
echo $sonde_id > pid_sonde
