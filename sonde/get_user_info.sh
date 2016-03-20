#!/bin/bash

# Boucle dans les utilisateurs connectes, sans doublons
for name in $( users | sed "s/ /\n/g" | sort | uniq )
do
    # Le nom de l'utilisateur est recu par parametre
    uid=$(id -u $name)

    who=$(who | grep $name | head -n1 | sed "s/\( \)\{1,\}/|/g")
    login_date=$(echo $who | cut -f3 -d"|")
    login_time=$(echo $who | cut -f4 -d"|")

    # Verifier si l'utilisateur peut gagner les droits de root
    isroot=0
    for gr in $(groups ricardo | sed "s/^\w* : //")
    do
        if [ "$gr"=="root" ] || \
           [ "$gr"=="adm" ] || \
           [ "$gr"=="admin" ] || \
           [ "$gr"=="sudo" ] || \
           [ "$gr"=="wheel" ]
        then
            isroot=1
            break
        fi
    done

    echo "$uid|$name|$isroot|$login_date $login_time"
    echo "2$uid|2$name|$isroot|$login_date $login_time"
done
