#language: fr

@initial-release @login
Fonctionnalité: Enregistrer un nouveau client

  *En tant que nouveau client du Shopozor,  
  je veux pouvoir y créer un compte avec un e-mail et un mot de passe,  
  afin d'avoir accès à toutes ses fonctionnalités.*  

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
    
  Scénario: Un utilisateur s'enregistre avec un e-mail déjà connu

    Si un utilisateur tente de s'enregistrer avec un e-mail déjà connu du Shopozor, 
    il faut notifier le client correspondant à cet e-mail et inscrire l'incident 
    dans un journal car il se peut que ce client soit en train de se faire pirater 
    son compte.     
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec un e-mail déjà connu
    Alors un message d'avertissement est envoyé à cet e-mail
    Et le Shopozor enregistre l'incident dans son journal
    
  Scénario: Le client communique son mot de passe dans les temps
    
    Une fois que le client a suivi le lien de confirmation, il peut renseigner son mot de passe. 
    A la validation de celui-ci par le Shopozor, son compte s'active et son mot de passe s'y associe. 
    
    Etant donné un client qui a reçu un lien de confirmation de création de compte
    Lorsqu'il définit son mot de passe dans les temps
    Alors son compte est activé
    Et son mot de passe est sauvegardé
    Mais il n'est pas identifié
    Et son lien de confirmation est invalidé
   
  Scénario: Le client confirme son adresse e-mail trop tard

    En plus de n'être utilisable qu'une seule fois, le lien expire après un certain temps 
    pour des raisons de sécurité. 
    
    Etant donné un client qui a reçu un lien de confirmation de création de compte
    Lorsqu'il définit son mot de passe trop tard
    Alors il obtient un message stipulant que le lien a expiré
    Et son compte n'est pas activé

  Scénario: Le client suit le lien de création de compte une deuxième fois
    
    Le lien de confirmation de création de compte ne peut être utilisé qu'une seule fois. 
    Si le client désire modifier son mot de passe, il doit utiliser la fonctionnalité 
    "mot de passe oublié". 
    
    Etant donné un client qui reçu un lien de confirmation de création de compte
    Lorsqu'il définit son mot de passe pour la deuxième fois
    Alors il obtient un message stipulant que le lien a expiré
    Et son mot de passe reste inchangé