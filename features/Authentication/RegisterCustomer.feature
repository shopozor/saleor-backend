#language: fr

@initial-release @auth @signup @wip
Fonctionnalité: Enregistrer un nouveau client

  *En tant que nouveau client du Shopozor,  
  je veux pouvoir y créer un compte avec un e-mail et un mot de passe,  
  afin d'avoir accès à toutes ses fonctionnalités.*  

  ![Processus d'enregistrement](UserRegistration.png)
  
  Scénario: Le client est nouveau

    Le client potentiel commence par donner un e-mail qu'il devra valider en visitant un 
    lien de confirmation qui lui y sera envoyé. Dans l'intervalle, un compte inactif et 
    sans mot de passe lui est créé.  
    
    Le lien est du type 
  
    <pre>http://www.shopozor.ch/activate/encodedUserId/token</pre>
    
    Lorsqu'un client inconnu fait une demande d'enregistrement
    Alors il reçoit un e-mail avec un lien d'activation de compte
    Et son compte est créé
    Mais il est inactif
    
  @user-accounts  
  Scénario: Le client a déjà un compte inactif
    
    Le client qui a déjà enregistré son e-mail mais n'a pas réussi à consulter 
    son lien de confirmation dans les temps conserve un compte inactif. Il peut alors
    refaire une demande d'enregistrement et obtenir un nouveau lien d'activation de compte. 
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte inactif
    Alors il reçoit un e-mail avec un lien d'activation de compte    
    
  @HackerAbuse @user-accounts
  Scénario: Un utilisateur s'enregistre avec l'e-mail d'un compte actif

    Si un utilisateur tente de s'enregistrer avec un e-mail lié à un compte déjà actif, 
    il faut notifier le client correspondant à cet e-mail et inscrire l'incident 
    dans un journal car il se peut que ce client soit en train de se faire pirater 
    son compte.  
    
    Aucun message d'erreur n'est retourné afin de donner le moins d'information possible 
    à un potentiel pirate. 
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte actif
    Alors il n'obtient aucun message d'erreur
    Alors un message d'avertissement est envoyé à cet e-mail
    Et l'incident est enregistré dans un journal

  Scénario: Le nouveau client définit un mot de passe conforme dans les temps
    
    Au moment où l'utilisateur définit son mot de passe, la validité du lien est vérifiée. 
    Dès que le mot de passe est défini, le lien d'activation est invalidé. Si le mot de passe 
    est conforme à la politique relative aux mots de passe, le compte du client est activé.
    
    # Pour débuter, nous pouvons utiliser le [default_token_generator](https://github.com/django/django/blob/master/django/contrib/auth/tokens.py). 
    # Il réagit au paramètre `PASSWORD_RESET_TIMEOUT_DAYS`. 

    # Comme le mot de passe de l'utilisateur est modifié, ses données changent, donc son token s'invalide. Voir 
    # [cet exemple](https://simpleisbetterthancomplex.com/tutorial/2016/08/24/how-to-create-one-time-link.html)
    # pour plus d'infos.
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte avec un mot de passe conforme au plus tard 1 jour après sa réception
    Alors son compte est activé
    Et son mot de passe est sauvegardé
    Et son lien d'activation est invalidé
    Mais il n'est pas identifié
    
  @HackerAbuse  
  Scénario: Le nouveau client définit un mot de passe non conforme dans les temps
    
    Si l'utilisateur entre un mot de passe non conforme, cela signifie qu'il a contourné les vérifications 
    de l'application client. Dans ce cas, son compte est supprimé, ce qui invalide automatiquement son lien 
    d'activation. Il peut refaire une demande d'enregistrement avec le même e-mail et recommencer le processus.
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte avec un mot de passe non conforme au plus tard 1 jour après sa réception
    Alors son compte est supprimé
    Et son lien d'activation est invalidé
    
  Scénario: Le nouveau client active son compte une deuxième fois
    
    Le lien de confirmation de création de compte ne peut être utilisé qu'une seule fois, 
    dans un certain laps de temps. Si le client désire modifier son mot de passe une fois 
    qu'il l'a défini, il doit passer par la fonctionnalité "mot de passe oublié".
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Et qui a déjà activé son compte
    Lorsqu'il l'active pour la deuxième fois
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son mot de passe reste inchangé
    
  Scénario: Le nouveau client active son compte trop tard 
    
    En plus de n'être utilisable qu'une seule fois, le lien expire après un certain temps. 
    Dans ce cas, l'utilisateur reste inactif et sans mot de passe, i.e. son compte n'est pas supprimé.
    Il a toujours la possibilité d'activer son compte en refaisant une demande d'enregistrement pour 
    obtenir un nouveau lien.  
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte avec un mot de passe conforme 2 jours après sa réception
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son compte reste inactif