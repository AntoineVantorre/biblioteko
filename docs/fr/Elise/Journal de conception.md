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


