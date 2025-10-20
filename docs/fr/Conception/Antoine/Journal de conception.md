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