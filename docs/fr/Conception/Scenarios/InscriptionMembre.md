## (cas de base) : Un utilisateur souhaite s'inscrire

- Description:

Un utilisateur veut s'inscrire

Listes des acteurs:

    Membre, Application, Bibliothécaire

Prérequis:

    Le membre n'est pas inscrit

Données:

1) Entrée

    informations personnelles de l'utilisateur (nom prenom age mail mdp)

2) Sortie

    "identité créée dans le registre"

Étapes:

    1. Le membre demande l'enregistrement de son identité
    2. L'application verifie qu'il n'en fait pas deja parti (mail non attaché)
    3. Membre enregistré

## (cas erreur) : Un utilisateur deja inscrit veut s'inscrire

- Description:

Un membre veut s'inscrire (il l est deja)

Listes des acteurs:

    Membre, Application

Prérequis:

    Le membre n'est pas inscrit

Données:

1) Entrée

    informations personnelles de l'utilisateur (nom prenom age mail mdp)

2) Sortie

    "identité créée dans le registre"

Étapes:

    1. Le membre demande l'enregistrement de son identité
    2. L'application verifie qu'il n'en fait pas deja parti (mail non attaché)
    3. Mail deja enregistré
    4. Reinitialisation du mdp par mail

