Rapport google docs : https://docs.google.com/document/d/1sNq7CFEwSVqyef5PRLKkL1l1qhyQWo0Uw3KBJGJMnHE/edit#
# mami
MAMI (Monitoring Application Made Ici)

<img src="https://github.com/uy-rrodriguez/mami/blob/master/mami.png" height="350px" alt="logo mami"/>

_http://www.clipartlord.com/2015/02/10/free-cute-cartoon-granny-clip-art/_

--------------------------------------------------------------------------------

# Stockage de données
## Base de données

Cette section présente la structure de la base de données qui stocke l'information associée à chaque
machine où il y a une sonde installée.

La table Server représente une machine. Stat est la table qui stocke l'historique
utilisé pour les statistiques, chaque enregistrement correspond à une machine à un
instant donné. StatDisk stocke l'information des partitions d'une machine à un
instant donné.

Les tables User et Process sont utilisées pour enregistrer d'autres informations
utiles sur chaque machine, correspondantes à la dernière collecte d'information.
À chaque lecture d'un fichier XML, les anciennes données dans ces tables sont
supprimées. User stocke les utilisateurs connectés sur une machine à un instant
donné, pendant que Process stocke les 10 processus les plus gourmands.


### Server #####################################################################

|Nom             |Type          |Clé  primaire|
|----------------|--------------|-------------|
|name            |VARCHAR(50)   |PRIMARY KEY  |
|ip              |VARCHAR(15)   |             |
|uptime          |VARCHAR(10)   |             |


### Stat #######################################################################

|Nom             |Type          |Clé  primaire|
|----------------|--------------|-------------|
|server_name     |VARCHAR(50)   |PRIMARY KEY  |
|date            |DATE          |PRIMARY KEY  |
|cpu_used        |FLOAT         |             |
|ram_used        |INT           |             |
|ram_total       |INT           |             |
|swap_int        |INT           |             |
|swap_total      |INT           |             |
|processes_count |INT           |             |
|zombies_count   |INT           |             |
|users_count     |INT           |             |

* FOREIGN KEY server_name REFERENCES (Server.name)


### StatDisk ###################################################################

|Nom             |Type          |Clé  primaire|
|----------------|--------------|-------------|
|server_name     |VARCHAR(50)   |PRIMARY KEY  |
|date            |DATE          |PRIMARY KEY  |
|mnt             |VARCHAR(20)   |PRIMARY KEY  |
|used            |INT           |             |
|total           |INT           |             |

* FOREIGN KEY server_name REFERENCES (Stats.server_name)
* FOREIGN KEY date REFERENCES (Stats.date)


### User #######################################################################

|Nom             |Type          |Clé  primaire|
|----------------|--------------|-------------|
|server_name     |VARCHAR(50)   |PRIMARY KEY  |
|uid             |INT           |PRIMARY KEY  |
|name            |VARCHAR(20)   |             |
|isroot          |BOOLEAN       |             |
|login_time      |DATE          |             |

* FOREIGN KEY server_name REFERENCES (Server.server_name)


### Process ####################################################################

|Nom             |Type          |Clé  primaire|
|----------------|--------------|-------------|
|server_name     |VARCHAR(50)   |PRIMARY KEY  |
|pid             |INT           |PRIMARY KEY  |
|command         |VARCHAR(200)  |             |
|username        |VARCHAR(20)   |             |
|cpu             |FLOAT         |             |
|ram             |INT           |             |

* FOREIGN KEY server_name REFERENCES (Server.server_name)


--------------------------------------------------------------------------------







