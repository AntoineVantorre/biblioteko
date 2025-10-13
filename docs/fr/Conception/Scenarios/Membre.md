# Devenir "Utilisateur"

- Description:

Une personne veut devenir Utilisateur, il doit s authentifier via son adresse mail

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

# Devenir "Membre"

- Description:

Un utilisateur veut devenir membre, il doit s'authentifier via france connect
Cette inscription lui permet de publier des fichiers numeriques

Listes des acteurs:

    - Utilisateur / futur membre
    - Système d'authentification FranceConnect
    - Bibliothèque numérique

Prérequis:

    L'utilisateur a un compte FranceConnect

Données:


Étapes:

    1. Le membre demande l'authentification via FranceConnect
    2. L'application redirige l'utilisateur vers l'interface FranceConnect pour authentification
    3. {Suite de flux entre user et FranceConnect}... FranceConnect renvoit un token d'authentifiaction 

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

