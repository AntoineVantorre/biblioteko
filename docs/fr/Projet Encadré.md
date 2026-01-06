# PJE D Biblioteko : Rapport
## Elise Magnier et Antoine Vantorre

Ce document rassemble les idées contenues dans les journaux de conception individuels.
Pour la liste détaillée des journaux de conception, voir les fichiers de travail des membres du projet. 

## Description du sujet

Biblioteko est une application web permettant à ses utilisateurs de proposer des oeuvres numériques ou de les visionner, à la manière d'une bibliothèque numérique. Ainsi des libraires (modérateurs) s'occupent de modérer les oeuvres proposées, afin qu'elles soient conforment à la loi, notamment sur les droits d'auteur. Les utilisateurs peuvent soumettre des livres scannés sous forme de pdf, qui seront retranscrits en markdown pour une lecture facilitée sur un écran. 

## Premières séances 

Les premières séances se sont concentrées sur l'analyse du sujet et la définition de ses limites, ainsi que sur le développement de l'outil de transcription markdown d'un pdf.

Les tâches se sont naturellement réparties, Elise se chargeant de la transcription en markdown et Antoine de l'analyse du sujet. 

### Outil de transcription de pdf en markdown

Cet outil a été réalisé en python. Il peut-être appelé en précisant le fichier d'entrée et le répertoire de sortie en ligne de commande.

L'outil OCR utilisé pour la transcription est l'API de Mistral, plus particulièrement un agent Mistral avec un prompt adapté aux tâches qui lui sont demandées. 

Nous avons utilisé Mistral car il est efficace et propose une utilisation gratuite jusqu'à un certain nombre de requêtes. De plus l'entreprise est française, ce qui est un avantage pour notre projet qui démarre en France.

La principale difficulté a été de comprendre comment assembler le fichier markdown reçu, car les requêtes à l'API Mistral ont une limite de taille et il est donc impossible de traiter un livre entier d'un coup. 

Une autre difficulté rencontrée est de faire face aux changements constants de l'API. En effet, Mistral étant une entreprise relativement jeune et en pleine expansion, il est très fréquent que l'interface de l'API ou ses conditions d'utilisation changent brusquement, plus particulièrement pour les utilisateurs qui ne paient pas. 

Une attention particulière a été apporté à l'inclusion d'images dans le fichier markdown produit, de sorte que ce fichier contienne également les schémas et dessins originaux. 

### Analyse du sujet

L'analyse du sujet s'est faite sur plusieurs semaines. En effet, il a fallu bien définir chaque terme, trouver et définir les différents scénarios. La liste des scénarios n'est pas exhaustive, car une telle application en possède énormement et le projet demande plus de ressources de développement que nous avons. 

En effet, l'analyse du sujet a révélé sa taille réelle, notamment son coût en temps. Nous n'avons pas le temps nécessaire pour réaliser tout le projet. Nous nous sommes donc concentrés sur une première version, simplifiée, afin de montrer au client le fonctionnement global de l'application. 

La création des scénarios et des glossaire a également relevé un aspect important du développement en entreprise : la communication. En effet, lors de la mise en commun de nos idées sur la modération des oeuvres protégées par le droit d'auteur, nous n'étions pas vraiment d'accord. Antoine souhaitait mettre en place la dispersion d'une oeuvre protégée en citations sur le web, notamment avec IFPS, pour rassembler ces citation afin de proposer l'oeuvre complète. Elise souhaitait mettre en place une modération automatique complétée par une modération manuelle (par les bibliothécaires) afin de ne proposer que des oeuvres libres de droits sur biblioteko. 

Face à ce désaccord, et en comparant avec les solutions des autres groupes, nous avons opté pour la solution d'Elise, qui est plus sûre légalement et également plus simple à mettre en place avec nos moyens limités. Antoine a cependant ajouté l'utilisation de protocoles de sécurité notamment le chiffrement pour garantir que nos fichiers ne soient pas recopiables par d'autres utilisateurs. Cet aspect n'est pas implémenté dans la première version du projet, par manque de temps, mais il pourra être mis en place dans une future version. 

### Diagrammes UML

L'étape suivante est la conception des diagrammes UML. Ces diagrammes sont importants car ils définissent le format de la donnée dans notre application, et la relation entre les différents éléments.

Un concept en particulier a été le fruit de plusieurs débat et sa modélisation a changé plusieurs fois. Ce concept et le modèle des utilisateurs : utilisateur, membre, bibliothécaire et administrateur. La solution retenue est la suivante :

- `Utilisateur` est le type de base.
- `Membre` est un utilisateur qui peut emprunter et proposer des œuvres.
- `Bibliothécaire` hérite des droits de `Membre` pour la modération des oeuvres, avec une règle empêchant un bibliothécaire de modérer ses propres soumissions. 
- `Administrateur` est une entité séparée avec des droits systémiques (gestion des comptes, assignation des rôles).

### Architecture du backend et base de données

La prochaine étape était la mise en oeuvre du back et frontend de l'application. Nous nous sommes réparti les tâches et avons travaillé en parallèle.  

Pour le backend nous avons choisi FastAPI pour sa simplicité et ses performances en traitement asynchrone. L'architecture suit une séparation en couches (routes, services, repositories, modèles/schemas) inspirée d'une architecture hexagonale afin d'améliorer la maintenabilité.

**Base de données :**
En ce qui concerne la base de données, plusieurs options ont été étudiées. MongoDB a d'abord été utilisée pour sa facilité et son intégration asynchrone via motor. 
Toutefois, après une discussion avec le professeur et la consultation d'IAs comme Gemini, les limitations sur les jointures et les besoins en requêtes relationnelles nous ont poussés à migrer vers PostgreSQL pour cette première version du projet. L'ORM `SQLModel` a été retenu pour faciliter l'écriture des modèles et des migrations.

**Modularité & conteneurisation :**
Afin de tirer partie de la modularité de l'application, et de faciliter sa gestion, nous avons packagé le backend et le frontend avec Docker. Les deux conteneurs communiquent entre eux et sont gérés avec `docker compose`. Cela permet de lancer l'ensemble avec une seule commande `docker compose up --build` et d'arrêter sans perdre les données avec `docker compose down`. 

Cela permet également de simuler une future architecture ou le frontend et le backend (notamment la base de données) seront sur des serveurs différents, ce qui est une architecture classique dans l'industrie. 

## Sécurité et authentification

La première version du projet implémente une authentification par tokens (à améliorer ultérieurement). L'intégration de FranceConnect a été étudiée pour la suite afin d'assurer l'unicité des comptes et une authentification nationale, mais n'est pas déployée dans la première version car trop complexe pour les moyens actuels.

Des pistes futures pour limiter la copie non autorisée ont été explorées : chiffrement sélectif des fichiers, watermarking ou chiffrement par clé par utilisateur. Ces mécanismes sont documentés comme améliorations possibles mais n'ont pas été implémentés par manque de temps.

### Stockage des oeuvres numériques

Nous avons évoqué plusieurs fois le stockage sur Git des oeuvres. Cette piste n'est pas écarté, et permet une vraie décentralisation de cette partie de l'application. Cependant, nous n'avons pas implémenté de stockage des fichiers soumis pour le moment. 

## Limitations, retours et perspectives

- L'outil de transcription est fonctionnel pour des ouvrages de taille limitée ; la gestion d'œuvres très volumineuses aec Git (> 2 Go) nécessite une stratégie de stockage différente (dépôt par œuvre, découpage).
- La limitation aux oeuvres libres de droits limite le champs de notre bibliothèque. De plus, la plupart oeuvres libres de droits sont facilement trouvable sur internet aujourd'hui. Il faudrait trouver un moyen d'intégrer des oeuvres protégées de manière légale et sécurisée. 
- Les évolutions souhaitables : intégration FranceConnect, conversion d'images complexes/figures en diagramme svg, robustesse face aux changements de l'API Mistral, et mécanismes de protection des fichiers (watermarking, chiffrement contrôlé).

## Conclusion

Le travail réalisé au cours de ce projet nous a appris beaucoup de chose sur le développement d'application en entreprise. Nous avons également tiré quelques leçons par rapport aux qualités d'un développeur full-stack. Il ne faut pas sous-estimer la taille d'un tel projet, et rester organisé avec des objectifs clairs. Il reste de nombreuses améliorations à faire mais nous avons pu livrer une partie du projet fonctionnelle. 


