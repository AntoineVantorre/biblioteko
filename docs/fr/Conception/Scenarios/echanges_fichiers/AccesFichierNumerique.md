## (cas de base) Emprunt d'un fichier numerique (classique)

- Description:

Le membre emprunte un fichier numérique disponibe dans la bibliotheque.

Listes des acteurs:

    Membre, Application, Bibliothécaire

Prérequis:

    Le membre est inscrit et connecté; le fichier est disponible à l'emprunt.

Données:

1) Entrée

    identifiant du membre
    identifiant du fichier

2) Sortie

    confirmation d'emprunt
    mise a jour du dépot

Étapes:

    1. Le membre demande l'acces au fichier
    2. L'application verifie la disponibilité du fichier
    3. Renvoie un refus OU BIEN enregistre l'acces au fichier de la part du membre
    4. Le membre a acces au livre dans son espace perso



## (cas erreur): Le membre souhaite recup un livre non reconnu

- Description:

Le membre emprunte un fichier numérique disponibe dans la bibliotheque.

Listes des acteurs:

    Membre, Application, Bibliothécaire

Prérequis:

    Le membre n'est pas inscrit ou n'est pas reconnu

Données:

1) Entrée

    identifiant du membre
    identifiant du fichier

2) Sortie

    "identifiant fichier non reconnu"

Étapes:

    1. Le membre demande l'acces au fichier
    2. L'application verifie la disponibilité du fichier
    3. Renvoie un refus car identifiant fichier invalide
    4. Le membre a le seum

## (cas erreur): Le membre n'est pas reconnu et souhaite faire qqchose

- Description:

Le membre emprunte un fichier numérique disponibe dans la bibliotheque.

Listes des acteurs:

    Membre, Application, Bibliothécaire

Prérequis:

    Le membre n'est pas inscrit ou n'est pas reconnu

Données:

1) Entrée

    identifiant du membre
    identifiant du fichier

2) Sortie

    "identifiant du membre non reconnu"

Étapes:

    1. Le membre demande l'acces au fichier
    2. L'application verifie la disponibilité du fichier
    3. Renvoie un refus car identifiant invalide
    4. Le membre a le seum