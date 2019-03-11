#language: fr

@initial-release @auth @signup @wip
Fonctionnalité: Enregistrer un nouveau client

  *En tant que nouveau client du Shopozor,  
  je veux pouvoir y créer un compte avec un e-mail et un mot de passe,  
  afin d'avoir accès à toutes ses fonctionnalités.*  

  ![Processus d'enregistrement](UserRegistration.png)
  
  Scénario: Le client est nouveau

    Le client potentiel commence par donner un e-mail qu'il devra valider en visitant un 
    lien de confirmation qui lui y sera envoyé. Dans l'intervalle, le Shopozor lui crée 
    un compte inactif sans mot de passe.  
    
    Le lien est du type 
  
    <pre>http://www.shopozor.ch/activate/encodedUserId/token</pre>
    
    Lorsqu'un client inconnu fait une demande d'enregistrement
    Alors il reçoit un e-mail avec un lien de confirmation de création de compte
    Et son compte est créé
    Mais il est inactif
    
  @HackerAbuse @user-accounts
  Scénario: Un utilisateur s'enregistre avec un e-mail déjà connu

    Si un utilisateur tente de s'enregistrer avec un e-mail déjà connu du Shopozor, 
    il faut notifier le client correspondant à cet e-mail et inscrire l'incident 
    dans un journal car il se peut que ce client soit en train de se faire pirater 
    son compte.  
    
    Aucun message d'erreur n'est retourné afin de donner le moins d'information possible 
    à un potentiel hacker. 
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec un e-mail déjà connu
    Alors il n'obtient aucun message d'erreur
    Alors un message d'avertissement est envoyé à cet e-mail
    Et le Shopozor enregistre l'incident dans son journal

  # TODO: rework the following scenarios' code  
  # TODO: we need a new mutation: verifyConfirmationLink(userId, token)
  # the mutation gives a new token back, based on the new user data (modified with the last login)
  
  Scénario: Le nouveau client consulte le lien de confirmation de création de compte dans les temps
    
    Au moment où l'utilisateur consulte son lien de confirmation, la validité du lien es vérifiée. 
    Dès qu'il est consulté, il est invalidé. L'utilisateur a alors besoin d'un nouveau token pour 
    la suite des opérations, à savoir le renseignement de son mot de passe.
    
    # Pour débuter, nous pouvons utiliser le [default_token_generator](https://github.com/django/django/blob/master/django/contrib/auth/tokens.py). 
    # Il réagit au paramètre `PASSWORD_RESET_TIMEOUT_DAYS`. 
    
    # Changer le champ last_login de l'utilisateur pour s'assurer que le token ne puisse plus correspondre 
    # à ses données originales.
    
    Etant donné un nouveau client qui a reçu un lien de confirmation de création de compte
    Lorsqu'il consulte son lien au plus tard 1 jour après sa réception
    Alors il reçoit un token d'initialisation de mot de passe
    Et son lien de confirmation est invalidé
    
  Scénario: Le nouveau client consulte le lien de confirmation de création de compte trop tard 
    
    En plus de n'être utilisable qu'une seule fois, le lien expire après un certain temps 
    pour des raisons de sécurité. 
    
    Etant donné un nouveau client qui a reçu un lien de confirmation de création de compte
    Lorsqu'il consulte son lien 2 jours après sa réception
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    
  Scénario: Le nouveau client consulte le lien de confirmation de création de compte une deuxième fois
    
    Le lien de confirmation de création de compte ne peut être utilisé qu'une seule fois, 
    dans un certain laps de temps. Si le client désire modifier son mot de passe, il doit 
    utiliser la fonctionnalité "mot de passe oublié".
    
    Etant donné un nouveau client qui a reçu un lien de confirmation de création de compte
    Et qui a déjà consulté son lien
    Lorsqu'il consulte son lien pour la deuxième fois
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    
  Scénario: Le nouveau client active son compte
    
    Une fois que le client a suivi le lien de confirmation, il peut renseigner son mot de passe si le lien 
    n'a pas expiré. A la validation du mot de passe, le compte du client s'active avec son mot de passe.
    
    Etant donné un nouveau client qui a consulté son lien de confirmation de création de compte dans les temps
    Lorsqu'il active son compte avec un mot de passe
    Alors son compte est activé
    Et son mot de passe est sauvegardé
    Et son token d'initialisation de mot de passe est invalidé
    Mais il n'est pas identifié
    