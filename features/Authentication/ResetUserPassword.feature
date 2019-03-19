# language: fr
  
Fonctionnalité: L'utilisateur réinitialise son mot de passe 

  *En tant qu'Utilisateur,  
  je veux pouvoir réinitialiser mon mot de passe  
  lorsque je l'ai oublié.*  
  
  # TODO: the user needs to provide her new password 
  
  # TODO: all the scenarios below belong to the ResetUserPassword feature!  
  # TODO: adapt the scenario titles and steps accordingly!
    
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