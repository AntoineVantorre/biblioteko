### Scénario 1 — Validation d’une œuvre par un bibliothécaire

**Description :**  
Une œuvre proposée par un membre doit être validée avant sa mise à disposition dans le fond commun.  
Le bibliothécaire consulte les fichiers en attente et décide d’approuver ou de rejeter l’œuvre selon les critères de conformité (qualité, légalité, métadonnées complètes).

**Acteurs :**  
- Bibliothécaire  
- Application (système de gestion)  
- Membre (contributeur)

**Prérequis :**  
- L’œuvre est dans le dossier `a_moderer`.  
- Les métadonnées ont été renseignées.  

**Données :**
1. **Entrée :**  
   - Identifiant de l’œuvre  
   - Identifiant du membre  
   - Métadonnées (titre, auteur, type, etc.)  

2. **Sortie :**  
   - Message de validation ou de rejet  
   - Déplacement du fichier dans le bon répertoire (`fond_commun` ou `séquestre`)  

**Étapes :**  
1. Le bibliothécaire ouvre la liste des œuvres à modérer.  
2. L’application charge les informations du fichier (métadonnées, aperçu du contenu).  
3. Le bibliothécaire vérifie la qualité du fichier et sa conformité légale.  
4. Si l’œuvre est conforme :  
   - L’application déplace le fichier dans `fond_commun`.  
   - Le membre reçoit une notification de validation.  
5. Si l’œuvre n’est pas conforme :  
   - Le fichier reste dans `a_moderer` ou est archivé dans `séquestre`.  
   - Le membre reçoit une notification de rejet avec motif.

### Scénario 2 — Rejet ou correction des métadonnées d’une œuvre

**Description :**  
Lors de la modération, le bibliothécaire peut rejeter une œuvre si les métadonnées sont incomplètes ou erronées,  
ou bien les corriger directement avant publication.

**Acteurs :**  
- Bibliothécaire  
- Application  
- Membre  

**Prérequis :**  
- Le fichier est en attente dans `a_moderer`.  
- L’œuvre n’a pas encore été validée.  

**Données :**
1. **Entrée :**  
   - Métadonnées existantes  
   - Corrections éventuelles du bibliothécaire  

2. **Sortie :**  
   - Nouvelles métadonnées validées  
   - Notification au membre  

**Étapes :**  
1. Le bibliothécaire consulte les métadonnées associées à l’œuvre.  
2. Il identifie les champs manquants (ex : auteur, catégorie, année).  
3. Il corrige ou complète les métadonnées directement dans l’application.  
4. L’application enregistre les modifications et met à jour le fichier de métadonnées.  
5. Le bibliothécaire choisit de valider l’œuvre ou de la renvoyer au membre pour correction.  
6. Le membre est notifié de la décision.

### Scénario 3 — Transfert d’une œuvre du séquestre vers le fond commun

**Description :**  
Une œuvre sous droit, conservée temporairement dans le dossier `séquestre`, devient libre de droit à une date donnée.  
Le système (ou un bibliothécaire) la transfère alors automatiquement vers le fond commun pour diffusion à tous.

**Acteurs :**  
- Application (automatisation planifiée)  
- Bibliothécaire  

**Prérequis :**  
- L’œuvre est stockée dans `séquestre`.  
- La date d’expiration des droits est atteinte.  

**Données :**
1. **Entrée :**  
   - Identifiant de l’œuvre  
   - Date d’expiration des droits  

2. **Sortie :**  
   - Œuvre déplacée dans `fond_commun`  
   - Mise à jour du registre des œuvres  
   - Notification au bibliothécaire (et éventuellement au contributeur)

**Étapes :**  
1. L’application vérifie régulièrement les œuvres du `séquestre`.  
2. Pour chaque œuvre, elle compare la date actuelle à la date d’expiration des droits.  
3. Si la date est dépassée :  
   - L’application déplace l’œuvre vers `fond_commun`.  
   - Elle met à jour les métadonnées (“statut = libre de droit”).  
   - Une notification est envoyée au bibliothécaire.  
4. Le bibliothécaire peut vérifier la validité du transfert dans le journal des opérations.