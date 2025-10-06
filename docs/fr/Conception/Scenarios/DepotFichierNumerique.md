## (cas de base) Depot d'un fichier numerique en libre acces dans la base de données

Le membre envoit un fichier (scan du livre) pour le proposer aux autres membres

Listes des acteurs:

    Membre, Application, Bibliothécaire

Prérequis:

    Le membre est inscrit et connecté; le fichier scan est lisible et correspond bien a son livre

Données:

1) Entrée

    identifiant du membre
    fichier scan

2) Sortie

    confirmation d'enregistrement
    identifiant d'enregistrement

Étapes:

    1. Diviser le scan en plusieurs fichiers
    2. Envoyer demander retranscription de ces fichiers scan a l'API mistral
    3. Enregistre le texte obtenu par l'API dans un fichier .md dédié au livre du membre
    4. Associe un identifiant unique a ce fichier obtenu pour le proposer en libre acces