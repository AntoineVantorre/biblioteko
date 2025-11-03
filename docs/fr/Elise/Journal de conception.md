# Journal de conception
### Elise Magnier

*22/09/2025*
## Test d'utilisation de l'API Mistral "Pixtral" pour la reconnaissance de texte depuis un scan de livre sous forme pdf. 

-> Dans le dossier src, fichier ``transcribe_pdf.py``

**Etapes** : 
- Création d'un agent suivant le modèle Pixstral (large), avec comme instructions de transcrire sous format markdown le texte des images qui lui sont envoyées, en étant le plus fidèle possible au texte original.
- Création d'une clé API Mistral
- Création du fichier de test Python
- Transformation des pages du pdf en images (png), car l'API de mistral n'accepte pas les pdf
- Construction et envoi de la requête pour un fichier de test (exemple fournit par l'enseignant)
- Affichage de la réponse de l'IA : le texte formatté en markdown.

**TO DO** : 
- Transformer le code d'appel à l'API en programme CLI, pour permettre les tests
- Afficher le résultat de la requête à l'API au fur et à mesure de la réponse, et non en une fois à la fin
- Envoyer des requêtes par groupe de pages, afin de traduire le livre complet. 
- (**bonus**) Afficher / Renvoyer un état de la progression de la transcription.

## Analyse du sujet : Glossaire et définition des scénarios
Analyse du sujet du PJE, mots par mots. Construction du glossaire sous forme de tableau.

-> Dans le dossier ``docs/fr/Conception``, fichiers ``Glossaire.md``, ``Scénarios.md`` et ``Analyse du cahier des charges.md``

**TO DO** : 
- Terminer l'analyse
- Comparer avec mon duo de la Dream Team


*29/09/2025*
## Amélioration de la transcription avec l'API de Mistral 

### Améliorations :
- Ecriture du résultat dans un fichier .md
- Envoie des pages du pdf en batch de 5 (le maximum est 8, mais 5 semble bien fonctionner)
- Lancement du programme en ligne de commande (options -i pour input et -o pour l'output)
- Affichage d'une barre de chargement dans le terminal

### Difficultés : 
- Faire en sorte que l'agent IA garde en mémoire le contexte des dernières réponses, de façon à ce qu'il puisse terminer les phrases coupées entre deux pages.
    * Pour faire cela, on envoie avec chaque requête les trois dernières réponses de l'agent IA comme "contexte". J'ai également ajouté dans les instruction de l'agent, une instruciton lui demandant de faire attention au contexte notamment pour garder un formattage cohérent tout au long de la transcription.
- Trouver une façon de prendre en compte les pieds de page. 
    * Pour l'instant, l'agent IA Pixtral écrit les pieds de page comme un paragraphe au milieu du texte (dans l'ordre dans lequel il arrive dans le livre).
- Gérer les images
    * Pour l'instant, les images ne sont pas gérées.


*06/10/2025*

### Améliorations : 
- Changement d'utilisation de l'API Mistral. Maintenant, au lieu d'utiliser l'agent pixtral et d'envoyer les pages 5 par 5 sous forme d'image, on utilise Mistral en téléchargeant sur l'api le fichier pdf, puis en passant l'url du fichier à la requête envers mistral.


### Difficultés : 
- J'ai eu quelques difficultés à essayer de récupérer les images et schémas du livre en utilisant l'agent pixtral. En discutant avec u autre groupe, j'ai décidé d'essayer différement avec la technique actuelle (en faisant un upload du fichier à transcrire sur l'api de mistral).
- Il faudrait ajouter à la requête une extraction des métadonnées du pdf afin de pouvoir construire le profil de l'oeuvre plus tard.



*13/10/2025*

Travail sur la récupération des images et schéma de la transcription. Fusion des branches git de notre groupe en vue de faire une pull request.

à faire : ajouter les refs des images à celles du dossier des images

*20/10/2025*

Travail sur la récupération des images dans la transcription, qui est à présent fonctionnelle. Il reste à passer le texte dans l'IA pour correction (rassemblement des mots coupés entre les pages, etc), chose qui ne fonctionne plus maintenant mais qui fonctionnait avant (je pense que c'est à cause d'un changement dans les conditions d'utilisation de l'API Mistral).



**Réflexions sur la gestion des oeuvres protégées par un droit d'auteur.**
- Chiffrement de l'oeuvre (dans quel contexte, comment et pourquoi ? ) -> Le chiffrement ne reste efficace que 10 ans en moyenne
- Hébergement des oeuvres dans un autre pays -> pas possible, c'est trop risqué
- découpage de l'oeuvre en citations et rassemblement -> pareil, trop risqué et complexe
- ne proposer que des oeuvres libres de droits d'auteurs -> ne répond pas au cahier des charges de biblioteko, et il faut tout de même trouver un protocol qui s'assure qu'aucune oeuvre protégé n'est téléchargée


Idée de prodécure de dépôt d'une oeuvre
- Dépose une oeuvre sur la plateforme
- vérifier dans la base des oeuvres déjà examinées (base qui peut se trouver sur internet, comme ISBN search) si l'oeuvre a déjà été marquée comme protégée ou non, en fonction de la date de mort de l'auteur (ou non)
- passage dans une IA qui va vérifier qu'il n'y a rien d'illégal dans l'oeuvre
- étape de modération :
    - seuls les modérateurs peuvent regarder l'oeuvre à ce stade
    - les modérateurs n'ont accès qu'à une vue 
    - une fois que l'oeuvre est acceptée par les modérateurs elle peut être mise en ligne si elle est libre de droits d'auteurs. Sinon, on supprime le contenu.

Nous nous sommes mis d'accord sur cette solution.


*3/11/2025*

Mise en commun des solutions trouvées par les différents groupes pour contourner la loi / traiter les oeuvres de manière légale.

Discussion sur le cryptage des documents en fonction des différents utilisateurs. IL y a deux solutions possibles : 
- Le document est crypté en autant d'exemplaire qu'il y a d'utilisateurs, avec leur clé privée respective. Ainsi, chaque utilisateur peut décrypter sa version du document. Souvent, un filligrane est ajouté au document pour pouvoir identifier le coupable si le document fuite. 
- Le document est crypté avec une clé aléatoire, cette clé est crypté avec la clé de chaque utilisateur dans un document séparé pour chaque utilisateur. Ainsi, lorsque l'utilisateur veut accéder au document, il cherche l'en-tête qui lui correspond et décrypte la clé à l'aide de sa clée privée. Il peut ensuite décrypter le document. 

Recherches sur DEEPSEEK OCR. Malheureusement ce modèle ne peut pas être installé sur la machine de la fac car il n'y a pas assez d'espace.

Nous avons mieux compris l'enjeux du projet au travers des discussions avec mon binôme et avec le professeur, qui est principalement d'apprendre de nouvelles choses. Nous avons donc deux options, soit on reste simple mais le projet doit fonctionner correctement, soit on décide d'être plus ambitieux en laissant place à de potentiels problèmes de fonctionnement. Il me semble qu'être plus ambitieux peut être plus gratifiant en terme d'apprentissage. Ces réflexions sont à aprofondir pour la prochaine fois. 

Pendant la prochaine séance, il faudrait mettre en place la modération des oeuvres avec l'IA (première étape de modération), afin d'avertir si une oeuvre contient du contenu illégal.