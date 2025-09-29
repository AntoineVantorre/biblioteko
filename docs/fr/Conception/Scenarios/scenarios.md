# Scénario 1: Emprunt d'un fichier numerique (classique)

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

# Scenario 2: Depot d'un fichier numerique en libre acces dans la base de données

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

# Scénario 3 (invalidité): Le membre n'est pas reconnu et souhaite faire qqchose

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

# Scénario 4 (invalidité): Le membre souhaite recup un livre non reconnu

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

