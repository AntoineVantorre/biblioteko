## Scénarios : Sécurité & Gestion d’accès  

### Scénario 1 — Vérification du rôle avant action (Contrôle d’accès)

**Description :**  
Le système doit vérifier les droits d’un utilisateur avant de lui permettre d’exécuter une action.  
Les rôles (Utilisateur, Membre, Bibliothécaire, Administrateur) déterminent les actions autorisées.  
Ce contrôle garantit que seules les personnes habilitées peuvent accéder à certaines ressources.

**Acteurs :**  
- Application  
- Utilisateur / Membre / Bibliothécaire  

**Prérequis :**  
- L’utilisateur est connecté.  
- Son rôle est enregistré dans le registre des comptes.  

**Données :**
1. **Entrée :**  
   - Identifiant utilisateur  
   - Jeton de session ou token d’accès  
   - Action demandée (ex : “proposer_oeuvre”, “valider_oeuvre”)  

2. **Sortie :**  
   - Autorisation accordée ou refusée  
   - Message de feedback  

**Étapes :**  
1. L’utilisateur envoie une requête pour exécuter une action.  
2. L’application identifie le rôle associé au compte via le token d’accès.  
3. Elle consulte la table des permissions (RBAC : Role-Based Access Control).  
4. Si le rôle a les droits requis :  
   - L’action est exécutée.  
   - Une trace de l’opération est enregistrée dans les logs.  
5. Sinon :  
   - L’accès est refusé.  
   - Un message “Permission non autorisée” est renvoyé à l’utilisateur.  

### Scénario 2 — Gestion sécurisée des sessions et tokens

**Description :**  
Lorsqu’un utilisateur ou un membre se connecte, l’application crée un token sécurisé pour gérer la session.  
Ce token est utilisé pour authentifier les requêtes ultérieures sans devoir redemander le mot de passe à chaque fois.

**Acteurs :**  
- Application  
- Utilisateur / Membre  

**Prérequis :**  
- L’utilisateur s’est connecté via une authentification valide (identifiants ou FranceConnect).  

**Données :**
1. **Entrée :**  
   - Identifiants de connexion ou token FranceConnect  
   - Données du compte  

2. **Sortie :**  
   - Token JWT (ou équivalent) valide pour une durée déterminée  
   - Message de confirmation de connexion  

**Étapes :**  
1. L’utilisateur saisit ses identifiants ou s’authentifie via FranceConnect.  
2. L’application vérifie la validité des identifiants.  
3. Si l’authentification réussit :  
   - Un token sécurisé est généré (JWT signé ou token chiffré).  
   - Le token est stocké côté client (session ou local storage sécurisé).  
4. L’utilisateur accède alors aux fonctionnalités selon son rôle.  
5. En cas d’inactivité prolongée ou de déconnexion :  
   - Le token est invalidé.  
   - L’utilisateur doit se reconnecter.  

**Cas d’erreur :**  
- Token expiré → redirection vers la page de connexion.  
- Token invalide → déconnexion forcée et message “session expirée ou invalide”.

### Scénario 3 — Réinitialisation sécurisée du mot de passe

**Description :**  
Un utilisateur ayant oublié son mot de passe peut en demander la réinitialisation.  
Le système envoie un lien sécurisé par e-mail pour définir un nouveau mot de passe.

**Acteurs :**  
- Utilisateur / Membre  
- Application  
- Serveur de messagerie  

**Prérequis :**  
- Le compte utilisateur existe dans le registre.  
- L’adresse e-mail est valide.  

**Données :**
1. **Entrée :**  
   - Adresse e-mail de l’utilisateur  

2. **Sortie :**  
   - Lien temporaire de réinitialisation envoyé par e-mail  
   - Confirmation d’envoi à l’écran  

**Étapes :**  
1. L’utilisateur clique sur “Mot de passe oublié ?”.  
2. L’application vérifie si l’adresse e-mail est associée à un compte existant.  
3. Si oui, elle génère un token de réinitialisation temporaire (valide 30 min).  
4. Un e-mail contenant le lien sécurisé est envoyé à l’utilisateur.  
5. L’utilisateur clique sur le lien, saisit un nouveau mot de passe.  
6. L’application valide et met à jour le mot de passe (haché et salé).  
7. Le token est invalidé après utilisation.  

**Cas d’erreur :**  
- Adresse e-mail non reconnue → message d’erreur générique (“Aucun compte associé à cet e-mail”).  
- Token expiré → message “Lien expiré, veuillez refaire la demande”.  

---
