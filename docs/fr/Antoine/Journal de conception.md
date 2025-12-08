# Antoine Vantorre

========================================
## 22 septembre 2025
### Fonction Python -> lecture du livre
La seance m'a rappellé a quel point les taches "complexes" sont sequencées en petites taches réalisées par des devs, puis publiées en open sources (souvent) pour une une utilisation privée de chaque developpeur.
Le code de la fonction qui lis un fichier fichier pdf et envoit des requetes a une API était un rappel utile de la facon de coder en python
Les recherches en amont  (ici comment fonctionnait l'api gemini) pour pouvoir l'exploiter dans le code etait pertinant et represente un réel aspect du developpeur (on ne connait jamais parfaitement le langage, les features qu'on doit utiliser)
L'importance et le mode d'utilisation du fichier .env était aussi un rappel important

### Analyse du sujet/ glossaire
D'autre part, le traitement et l'analyse du sujet est un bon moyen de s'assurer un avancement linéaire, sans mauvaise surprise, cela me parait prendre beaucoup de temps pour confirmer des notions qui peuvent parfois sembler intuitives/ claires...
La compréhention du sujet et le dialogue entre collègues est primordial pour une coopération efficace, permettant de clarifier les ambiguîtés et coordonner les taches au sein de l'equipe

========================================
## 29 Septembre 2025

Aujourd'hui, nous avons pris la decision de nous repartir le travail de la manière suivante:

    Élise s'occupe du code de lecture puisqu'elle est plus avancée et que son API semble plus adaptée a cette tache. (bien que les appels API semblent tres lents)

    Antoine s'occupe du glossaire et du diagramme UML car plus avancé sur l'analyse du sujet

Biensur, nous nous expliquerons nos travaux respectifs afin de comprendre au mieux le projet dans sa globalité et d'avancer en ccordination

### Glossaire
Le reperage des mots clefs du sujet etant deja fait, j'ai fait un tableau pour definir chacun des mots clefs, afin de mieux comprendre l'enjeu du sujet, et de clarifier les choses a long terme

### UML
j'ai **commencé** le diagramme UML, afin de nous eclairer sur la future base de données 

=========================================

## 6 septembre

Avancement sur le diagramme UML, je suis face a la problematique suivante:
    Je dois d abord comprendre au mieux le sujet pour adapter l'UML aux conditions

Relecture du sujet

=========================================
## 13 septembre 

En relisant le sujet, je me rend compte que je ne suis pas encore arrivé a l'etape de construction de l'UML,
    Je dois d'abord construire des Scenarios plus complexes et plus nombreux, afin de fixer la comprehension du probleme dans le temps, et de ne plus avoir de probleme de comprehension

=========================================

## 20 septembre

Aujourd'hui, on doit choisir un protocole qui nous permettra de contourner le droit d'auteur:
    Plusieurs choix:
        Chiffrement (dure 10 ans)
        Ebergement dans un pays laxiste (les lois puvent changer)
        Decouper l'oeuvre en pleind e petites citations (chacune legales)
        Se concentrer sur le fait d'etre certain de ne proposer que des livre libres de droit

Chaque personne du groupe (de 4 personnes) a reflechi a une solution differente, (Fares, Assane -> Encodage des données en entré) (Elise -> Verification par moderateur)
(moi -> couper le livre en plein de citations courtes)

Probleme rencontré: si je decoupe un livre soumis au droits d'auteurs et que je le propose aux utilisateur, l'anonymat que procure IPFS ne m'extrait pas de mes responsabilités de publication, il faut aussi savoir que meme si on pretend ou suppose que le livre est construit a partir de rien, et qu'il ressemble malencontreusement a une oeuvre soumise aux droit d'auteur, si l'oeuvre entre en concurence avec l'oeuvre privée, alors on peut deja esperer avoir un bon compagnon de cellule

Ma piste ne semble pas etre la bonne, je pense que mes camarades ont trouvé une situation sans blocage donc je choisis la meilleur des leurs
Fares et Assane sont bloqués sur la verification du livre, ils l'encodent directement et veulent le decoder a l envoie vers l'utilisateur
    Cela ne repond pas aux conditions
Elise semble avoir trouvé une bonne piste, on verifie deja si le livre est reconnu dans ISBN, puis on propose aux moderateurs une vue (et non pas le fichier en soit) pour empecher la copie et l'exploitation de ce fichier, une fois que ce fichier est validé, on le sauvegarde, sinon, on le supprime.
    Cela semble etre une bonne approche, il nous laisse la possibilité a l'avenir de modifier notre procedure et de verifier par IA.

On part sur une idée, mais on pourra toujours ajouter des couches de securité:
    Par exemple je pense a un encodage (clef publique, privée) qui empecherait les utilisateurs de connaitre l'identité d'un Editeur, mais permettrait d'associer Chacune de ses oeuvres ensemble: 
        L'editeur aurait alors une clef privée grace a laquelle il ajoute sa signature (codée) a la fin du fichier qu'il upload


### Anecdotes et culture G

Les imprimantes ont un filigrane unique, qui permet leur identité, il est aussi impossible d'imprimer des billets, car l'imprimante reconnait un "pattern" interdit, donc refuse le scan

IPFS =InterPlanity File System
Protocole decentralisé de stockage et de partage de fichier


On distingue deux choix quand on cree un site    OVH     loi dassi
    Hebergeur => tout le monde peut push du contenu chez l'hebergeur

On doit adapter nos choix technique par rapport a l'etat de l'art actuel : on se soumets aux lois actuelles, si elle change demain, c est moins grave que si on créé notre appli demain sans se soumettre aux lois de demain

Un professeur a le doit d'evoquer des protocoles illegaux pour nous mettre en garde
    Mais il n'a pas le doit de nous inciter a suivre un protocole illagal
        On entendra jamais le prof nous dire par exemple d'utiliser le protocole IPFS afin de contourner les droits d'auteurs et publier des oeuvre 
        Le protocole IPFS peut en revanche etre un moyen d'amplifier notre anonymat, ce qui peut constituer une barriere de securité supplementaire.

Histoire du directeur general de halstolm -> injustice

## 3 novembre

Nous avons beaucoup discuté sur l'importance des droits d'auteurs, de ce que cela implique que ca soit quand on créé quelque chose, et quand on utilise une oeuvre sans savoir si elle est rééllement no copyright

On a aussi mis en commun le travail de chaque groupe
    - j'ai donc partagé nos reflexions ce qui a permis aux autres de comprendre certaines problematiques

    - j'ai aussi relativisé la problematique lié au chiffrement: c est une solution temporaire (10 ans) mais qui peut etre allongé si on combine plusieurs protocole (on passe le fichier par plusieurs protocoles de chiffrement, ce qui peut augmenter la durée de vie, on peut faire un parallele avec une lettre dans une enveloppe, elle meme dans une enveloppe)

Je pose enfin des mots sur un probleme qui perciste depuis le depuis du developpement du projet: quelle est l'echelle du projet? (est ce qu'on a le temps et les ressources necessaire pour mettre en oeuvre un outils qui n'a pas besoin d'aide humaine? si je fais valider chaque oeuvre par les moderateurs, est ce que c est tenable? a long terme? est ce faisable autrement?)
C'est pour cette raison que je perdais du temps a reflechir a LA solution optimale, celle qui est tenable indefiniment sans aide humaine, mais chaque projet a ses contraintes propres et on doit s'y adapter, si le projet ne permet pas un tel developpement, inutile de chercher aussi loin; on créé une premiere version et on adaptera plus tard

La notation du projet se base sur le cheminement des idées a mettre en oeuvre, pas que au produit final:
    J avais peur de m'aventurer dans une BDD decentralisée, cela permet une "couche" d'anonymat, mais cela demande de l'investissement et une prise de risque, ce n'est pas une idée a proscrire, on peut toujours coumuler les solutions qu'on a chacun explosé lors du cours precedents (dechiffrement de courtes citations encodées en plus d'une moderation pour oeuvres soumises a droits d'auteur)

## 10 novembre

Avancement dans la conctruction de l'uml (diagramme de classe), debats sur le futur developpement:
    - Un membre = un utilisateur qui publie, il est authentifié par franceconnect
    - Un bibliothecaire: il est lui aussi authentifié par france Connect, il herite de membre. Il peut publier des oeuvre, on devra s'assurer qu'il ne peut pas verifier ses propres oeuvres
    - Un administrateur: ne possede pas les pleins pouvoirs, certaines fonctionnalitées ne sont pas pertinentes a implementer dans le cadre de l'admin
    
On laisse a l'admin la possibilité de gerer tout l'aspect systeme et utilisateur, tandis ce qu'on laisse au bibliothecaire la charge de gerer le contenu, les oeuvres.

Probleme UML: un bibliothecaire peut aussi etre membre? ils peuvent publier des oeuvres? mais ne peuvent pas valider leurs propres oeuvres? comment s'y prendre?
Initialement, j ai pensé a faire un decorateur, pour specifier qu'un bibliothecaire pouvait possiblement etre membre ou utilisateur. En parallele, je pensais deja faire en sorte de prouver une unicité de membre grace a FranceConnect, on ne peut pas creer deux comptes membres a partir du meme compte FranceConnect, car on forcerait l'id a etre le meme, on pourrait hasher les infos de l'utilisateur france Connect par exemple. le probleme, c est qu'avec un decorateur on devrait créer plusieurs instances pour la meme personne, une fois membre, une fois bibliothecaire, ce qui poserait probleme.
Utilisateur <- Membre <- Bibliothecaire <- Administrateur
Mais cela impliquerait des problemes de duplication des methodes, l'admin aurait des fonctionnalité non pertinentes, pourrait peut etre creer un nouveau profil admin etc
On prefere partir de l'idée de créer une Interface "Gestion_oeuvres" qui regroupe les fonctionnalités communes de "Administrateur" et de "Bibliothecaire"

## 17 novembre
On a malheureusement pas le temps de faires des diagrammes sur l'ensemble des scenarios etc, donc on en fait quelques uns sur 
- Diagramme de classe: on applique le snake case car destiné a du code python
- BPMN: pour accompagner chaque scenario, on decrit les actions des differents acteurs pour une activité complexe telle que l'inscription d'un membre
- Diagramme d'etat transition: Pour cette V0, le diagramme d etat des fichiers ne prend pas en compte des notions complexe du genre "comment/qui/ou est stocké le fichier numerique, on considere pour cette version que tout est stocké dans un unique repo commun, mais a l'avenir, on attribuera un repo pour chaque oeuvre (pour une v1), on peut supposer que dans des cas extremes, cela pourrait poser probleme sur des oeuvres lourdes de plus de 2Go, mais viable pour une V1, on pourra ensuite implementer une nouvelle maniere de stocker les oeuvres pour contrer ce probleme, en repartissant les oeuvres lourdes sur plusieurs repo.
- Diagramme de sequence: on a decrit ici les differentes etapes pour valider/ rejeter une nouvelles inscription pour devenir membre, le diagramme en question est relativement simple mais reflete une vrai complexité d'implementation avant de connaitre le fonctionnement de FranceConnect

## 1 decembre
Aujourd hui: mise en place du modèle de la base de donnée, en suivant une architecture hexagonale, elle separe les routes/ Database/ Modèles, car c est une convention qui a fait ses preuves, de part sa propreté de code et sa facilité d'evolution.
Je n'ai encore jamais fais de projet en python, donc j'utilise le Framwork FastAPI sous les conseils de ChatGPT, cela me permettra de developper mes connaissances, coder proprement et plus rapidement, en me permettant par exemple de convertir des données Python <-> JSON.
Lors du developpement du modèle de la bdd, un probleme survient: quel type d'heritage implementer?
    - Heritage simple (ajouter toutes les colonnes dont on aura possiblement besoin, quitte a en laisser des vides si l'utilisateur n'est pas du bon type) on devra verifier son role a chaque appel mais facile a implementer
    - Heritage multiple (creer un modele pour chaque type d'utilisateur, quitte a faire apparaitre des colonnes identiques dans plusieurs "tableaux" differents) mais MongoDb ne gere pas l'heritage automatiquement, ce qui peut entrainer des complications
    - Single Table Inheritance (une table parent et d autres pour lier des données complementaires)

On a donc choisis de faire un Heritage simple, ce qui nous permet de faire une seule collection MongoDb, ce qui nous permet de changer facilement les roles (utilisateur -> membre par exemple)

Le choix de MongoDb etait une erreur puisqu'il est limité en terme de jointure, le stockage assez lourd, supporte les transaction ACID que si on utilise un replicat set ou un clsuster, chose qu'on ne met pes encore en place, et les requetes complexes multi-entités sont très dures a mettre en place (ces requetes peuvent etre utilses si on veut pouvoir connaitre la liste d'utilisateurs ayant consultés un livre par exemple)
PostgreSQL semble plus adapté au projet: puissant pour les jointures, les transactions ACID, plus leger si optimisé, rapide en lecture et ecriture, adaptés aux requetes complexes multi-entités, bien que le schema soit plus rigide et que le scaling horizontal est complexe a mettre en place

Compehention technique des indexes en bdd pour faire de meilleurs choix conceptuels et ameliorer ma qualité de code

## 8 decembre
On decide d'utiliser l'ORM SQLModel car cela nous permettra d'ecrire moins de SQL, gerera automatiquement les relations entre tables, rajoute une couche de securité pour eviter les injections SQL, fais gagner du temps car facile a mapper.

docker compose build --no-cache
docker compose up
