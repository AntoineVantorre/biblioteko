# Analyse et  du sujet
## Reperage des mots clefs

<span style='background:#f984e5'>Concept</span> : Mot portant une signification pour le projet ;

<span style='background:yellow'>Nom propre </span>: Identifiant unique d'une chose ou d'une personne ;

<span style='background:green'>Action</span> : transformation de l'état ;

<span style='background:orange'>Propriété </span>: qualité, durée etc.

# Sujet : Conception et architecture d’une bibliothèque numérique décentralisée

## Présentation générale

Le projet consiste à <span style='background:green'>développer</span> une <span style='background:#f984e5'>bibliothèque d'œuvres numérisées</span>. Chaque <span style='background:yellow'>utilisateur</span> de la bibliothèque <span style='background:green'>peut proposer</span> des <span style='background:#f984e5'>fichiers</span><span style='background:orange'> numériques</span> et <span style='background:green'>demander</span> leur <span style='background:#f984e5'>partage</span>. Par exemple, les œuvres peuvent être des <span style='background:#f984e5'>livres</span> <span style='background:orange'>scannés</span> au format PDF, **il** se pose alors le problème de la <span style='background:#f984e5'>propriété intellectuelle</span> qui sera alors <span style='background:green'>**résolu**</span> par une <span style='background:#f984e5'>modération</span> de la part de <span style='background:yellow'>bibliothécaires.</span>

Pour des raisons de compatibilité avec l'existant, <span style='background:#f984e5'>le langage de développement</span> **<span style='background:green'>imposé</span> par le <span style='background:yellow'>client</span> est <span style='background:yellow'>Python</span>**.

Le **<span style='background:#f984e5'>framework web</span>** <span style='background:green'>retenu</span> côté serveur est **<span style='background:yellow'>Pyramid</span>**, et le <span style='background:#f984e5'>langage de templates</span> utilisé est **<span style='background:yellow'>TAL/METAL</span>** (hérité de Zope/Plone, garantissant la <span style='background:orange'>compatibilité</span> avec l'historique).

Côté client, le choix est laissé aux développeurs :

- soit <span style='background:yellow'>**SolidJS**</span>, un <span style='background:#f984e5'>framework</span> moderne « React-like » basé sur JSX, performant et flexible,
- soit <span style='background:yellow'>**Bootstrap**</span>, solution plus traditionnelle (« old school ») mais simple à mettre en œuvre et rapide pour prototyper.

Les documents **gérés** par l'application doivent l'être à travers un <span style='background:#f984e5'>dépôt Git</span> et non une <span style='background:#f984e5'>base de **données**</span> traditionnelle pour la raison **qu'à** terme devra être développé**e** une application permettant aux terminaux (ordinateur ou téléphone mobile)**,** de pouvoir disposer des textes sous forme d'une <span style='background:#f984e5'>arborescence de **fichiers**</span>. Pour ceux qui ne sont pas à l'aise avec Git, il existe une série de formations gratuites **:** [https://www.youtube.com/watch?v=0sGQgfUdCAY](https://www.youtube.com/watch?v=0sGQgfUdCAY)

Il est toutefois demandé que **chaque fonctionnalité soit développée de <span style='background:orange'>manière modulaire</span>**, indépendante du reste du système, et puisse être **utilisée et testée en ligne de commande** afin de faciliter l'intégration continue et la <span style='background:orange'>validation unitaire</span>.

Compte tenu des délais, l'usage de l'**intelligence artificielle** est **fortement recommandé**, mais il doit être **entièrement documenté et traçable**. Les conversations (prompts) feront l'objet de débats en classe. Pour préparer cela, les <span style='background:yellow'>étudiants</span> doivent, avant le cours, regarder et comprendre la vidéo : [**Les 4 étapes pour entraîner un <span style='background:yellow'>LLM</span>**](https://www.youtube.com/watch?v=YcIbZGTRMjI).

Ce projet sert de support pédagogique pour aborder les notions d'<span style='background:#f984e5'>**architecture logicielle orientée objet**</span>, de <span style='background:#f984e5'>**modélisation UML**</span>, de <span style='background:#f984e5'>**design patterns**</span>, et de <span style='background:#f984e5'>**documentation**</span>.

Pendant le cours, les <span style='background:yellow'>étudiants</span> travailleront en <span style='background:#f984e5'>**binômes hétérogènes**</span> (compétences et parcours différents). Chaque binôme aura pour mission de <span style='background:green'>prendre en charge</span> une partie de la conception et du développement, puis de <span style='background:green'>présenter</span> et de <span style='background:green'>justifier</span> ses choix.

Il est impératif de <span style='background:green'>respecter</span> les **extraits du cours d'Architecture des logiciels** donnés en annexes (rôles de l'architecte, conception OO, attributs de qualité, vues architecturales, documentation, importance du nommage, etc.).

---

### Contexte du projet

L’association **CultureDiffusion** souhaite réaliser une **bibliothèque numérique décentralisée**.

#### Objectifs fonctionnels :

- <span style='background:green'>Permettre</span> à chaque membre de numériser des œuvres au format pdf et de les proposer à l’emprunt.
- <span style='background:green'>Permettre</span> la reconnaissance de texte des œuvres numérisés via plusieurs IA (Gemini, Pixtral).
- Offrir un accès gratuit aux œuvres du domaine public.
- <span style='background:green'>Permettre</span> la location d’œuvres "numérique" sous droits pour une période de deux semaines.
- Diffuser automatiquement les œuvres devenues libres de droit à l’ensemble des membres disposant d’espace disque partagé.
- <span style='background:green'>Permettre</span> le téléchargement des oeuvres au format Markdown.
- <span style='background:green'>Gérer</span> le processus permettant aux bibliothécaires d'assurer la **modération** des œuvres déposées sur la plateforme par les membres (vérification, enrichissement des métadonnées, validation ou rejet).
- <span style='background:green'>Gérer</span> les droits et les copies selon la législation en vigueur.

#### Structure du dépôt de la bibliothèque (métaphore de répertoires) :

- `fond_commun` : œuvres libres de droits mises à disposition par l’association.
- `emprunts` : œuvres sous droit empruntées, chiffrées avec la clé du membre.
- `séquestre` : œuvres sous droit en attente, gérées par l’association, avec un accès restreint.
- `a_moderer` : œuvres proposées par les membres, en attente de validation par un bibliothécaire.

#### Classification des œuvres :

- **Livres** : BD, Romans, Jeunesse, Techniques, Éducation, Culture, Santé, etc.
- **Musique** : Classique, Jazz, Pop, Metal, etc.
- **Vidéos** : SF, Histoire, Séries, Documentaires, etc.
- **Articles**.  
    Une œuvre peut appartenir à plusieurs catégories simultanément.

### Travail demandé

#### Partie 1 : Analyse et glossaire

1. Identifier les **concepts** (entités, rôles, actions, propriétés) dans le cahier des charges.
2. Élaborer un **glossaire métier** et un **glossaire technique** (définitions claires, classées alphabétiquement).
3. Justifier vos choix de vocabulaire par rapport à l’importance du **noms et conventions de nommage (5.5)**.

#### Partie 2 : Modélisation UML

- Réaliser le **diagramme de cas d’utilisation** global.
- Lister les **scénarios fondamentaux** de l’application, en ajouter si nécessaire.
    - Exemple : installation de l’application, devenir membre, emprunter une œuvre, proposer une œuvre, reconnaître le texte et les schémas d’une œuvre, modérer une œuvre, consulter le fond commun, exporter une œuvre au format Markdown.
- Trier les scénarios par ordre d’importance.
- Produire **au moins 4 diagrammes de séquence système** des scénarios principaux, dont 2 qui n’auront été proposés par aucun autre binôme.
- Réaliser **5 diagrammes de classes** associés aux scénarios les plus critiques. 
- Produire un **diagramme de classes global** détaillant les associations et leurs cardinalités.
- Donner des **diagrammes d’activités** permettant de comprendre les processus documentaires (workflows).

#### Partie 3 : Choix d’architecture

1. Décrire l’**architecture logicielle** choisie (ex. architecture en couches, orientée services, micro-services simplifiés).
2. Justifier vos choix au regard des **attributs de qualité** (performance, sécurité, maintenabilité, modularité, évolutivité).
3. Identifier les **design patterns** utilisés (ex. Singleton, Factory, Observer, Strategy) et justifier leur pertinence dans ce projet.
4. Expliquer comment la **documentation** (chapitre 3 des annexes) sera intégrée dans le flux de travail du projet (usage de Markdown, Git, diagrammes UML intégrés).

#### Partie 4 : Nommage et qualité

1. Définir un **guide de nommage** adapté au projet (inspiré du §5.5 : cohérence, conventions, lisibilité).
2. Vérifier la cohérence entre :
    
    - le glossaire métier,
    - les classes et modules UML,
    - les scénarios,
    - la documentation.
        
3. Proposer l’usage d’**outils automatiques** (linters, règles de formatage, CI/CD pour la documentation) pour renforcer la qualité.
    

---

### Contraintes

- Utiliser **PlantUML** ou **Mermaid** ou **D2** pour vos diagrammes (l'IA peut faire de la conversion de diagramme, mais il faut vérifier la sémantique produite).
- Respecter les principes de **conception orientée objet** (encapsulation, héritage, polymorphisme).
- Intégrer explicitement les notions de **vues architecturales** (logique, processus, développement, physique).
- Documenter vos choix dans un **dépôt Git structuré** (voir chapitre 5 des annexes).

---

### Livrables attendus

1. Glossaire métier et technique (Markdown).
2. Diagramme de cas d’utilisation + scénarios détaillés (Markdown + PlantUML).
3. Diagrammes de séquence (PlantUML).
4. Diagrammes de classes (scénarios et global).
5. Document de justification des choix d’architecture et de design patterns.
6. Guide de nommage (Markdown).
7. Dépôt Git documenté avec arborescence conforme aux recommandations du cours.
8. Implémentation sommaire des principales fonctionnalités sous forme de scripts indépendants pouvant être intégrés en un tout ou utilisé indépendamment (prévoir l'usage des .env pour le paramétrage des clés permettant d’interroger les IA).
9. Tests unitaires
10. Tests d'intégrations.
11. Test de validations

